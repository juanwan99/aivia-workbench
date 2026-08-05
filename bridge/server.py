#!/usr/bin/env python3
"""Aivia edu-bridge (MODE=mock) — identity, read-only, proposals, audit.

Hard rules:
  - No AI write path to edu business DB
  - No /apply for agents
  - school_id isolation
"""
from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
import traceback
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import jwt

VERSION = "0.1.1"
WEAK_SECRETS = frozenset(
    {
        "",
        "dev-only-change-me-bridge-c",
        "change-me",
        "secret",
        "password",
        "jwt-secret",
    }
)

MODE = os.environ.get("BRIDGE_MODE", "mock")
HOST = os.environ.get("BRIDGE_HOST", "127.0.0.1")
PORT = int(os.environ.get("BRIDGE_PORT", "18090"))
JWT_SECRET = os.environ.get("BRIDGE_JWT_SECRET", "")
JWT_ISS = os.environ.get("BRIDGE_JWT_ISS", "bridge-mock")
JWT_TTL = int(os.environ.get("BRIDGE_JWT_TTL", "3600"))
# Optional gate for mock /auth/exchange (header X-Bridge-Exchange-Token or body exchange_token)
EXCHANGE_TOKEN = os.environ.get("BRIDGE_EXCHANGE_TOKEN", "").strip()
DATA_DIR = Path(os.environ.get("BRIDGE_DATA_DIR", str(Path(__file__).resolve().parent / "data")))
DB_PATH = DATA_DIR / "bridge.sqlite3"
AUDIT_PATH = DATA_DIR / "audit.jsonl"


def require_strong_secret() -> None:
    """F1: refuse to start with missing/weak JWT secret."""
    if not JWT_SECRET or JWT_SECRET in WEAK_SECRETS or len(JWT_SECRET) < 24:
        raise SystemExit(
            "[aivia-bridge] FATAL: BRIDGE_JWT_SECRET missing or weak. "
            "Set a long random value in ~/.secrets/bridge.env (never commit)."
        )
    if HOST not in ("127.0.0.1", "localhost", "::1") and not EXCHANGE_TOKEN and MODE == "mock":
        # non-loopback bind with open mock exchange is a high-risk misconfig
        print(
            "[aivia-bridge] WARN: non-loopback bind without BRIDGE_EXCHANGE_TOKEN; "
            "mock exchange is open to network peers.",
            flush=True,
        )

# Mock catalog (MODE=mock)
MOCK_CLASSES = {
    "school-demo": [
        {"id": "cls-101", "name": "高一(1)班", "grade": "高一"},
        {"id": "cls-102", "name": "高一(2)班", "grade": "高一"},
    ],
    "school-other": [
        {"id": "cls-x1", "name": "别校一班", "grade": "初二"},
    ],
}
MOCK_COURSES = {
    "school-demo": {
        "bio-pea": {
            "id": "bio-pea",
            "title": "豌豆杂交与遗传规律",
            "subject": "生物",
            "outline": ["性状分离比", "测交", "基因型推断"],
        },
        "math-linear": {
            "id": "math-linear",
            "title": "一次函数",
            "subject": "数学",
            "outline": ["定义", "图像", "应用"],
        },
    },
    "school-other": {
        "eng-1": {"id": "eng-1", "title": "别校英语", "subject": "英语", "outline": ["unit1"]},
    },
}

_lock = threading.Lock()


def _ensure_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS proposals (
              id TEXT PRIMARY KEY,
              school_id TEXT NOT NULL,
              author_sub TEXT NOT NULL,
              type TEXT NOT NULL,
              title TEXT NOT NULL,
              payload_json TEXT NOT NULL,
              status TEXT NOT NULL,
              created_at REAL NOT NULL,
              reviewed_by TEXT,
              review_note TEXT,
              reviewed_at REAL
            )
            """
        )
        conn.commit()


def _audit(event: dict[str, Any]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": time.time(),
        "mode": MODE,
        **event,
    }
    # never log secrets
    for k in list(row.keys()):
        if "token" in k.lower() or "secret" in k.lower() or "password" in k.lower():
            row[k] = "[redacted]"
    with _lock:
        with AUDIT_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def issue_token(sub: str, school_id: str, role: str, name: str = "") -> str:
    now = int(time.time())
    payload = {
        "sub": sub,
        "school_id": school_id,
        "role": role,
        "name": name or sub,
        "iss": JWT_ISS,
        "iat": now,
        "exp": now + JWT_TTL,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def verify_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"], issuer=JWT_ISS)


class Handler(BaseHTTPRequestHandler):
    server_version = f"aivia-bridge/{VERSION}"

    def log_message(self, fmt: str, *args: Any) -> None:
        # quieter access; business audit is separate
        pass

    def _json(self, code: int, obj: Any) -> None:
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Bridge-Mode", MODE)
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict[str, Any]:
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0:
            return {}
        raw = self.rfile.read(n)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return {}

    def _bearer(self) -> str | None:
        auth = self.headers.get("Authorization") or ""
        if auth.lower().startswith("bearer "):
            return auth.split(" ", 1)[1].strip()
        return None

    def _principal(self) -> tuple[dict[str, Any] | None, str | None]:
        tok = self._bearer()
        if not tok:
            return None, "missing_token"
        try:
            p = verify_token(tok)
            return p, None
        except jwt.ExpiredSignatureError:
            return None, "expired"
        except Exception:
            return None, "invalid"

    def do_GET(self) -> None:  # noqa: N802
        try:
            self._dispatch("GET")
        except Exception as e:
            _audit({"level": "error", "err": str(e), "path": self.path})
            self._json(500, {"error": "internal", "message": "服务内部错误"})

    def do_POST(self) -> None:  # noqa: N802
        try:
            self._dispatch("POST")
        except Exception as e:
            _audit({"level": "error", "err": str(e), "path": self.path, "tb": traceback.format_exc()[-500:]})
            self._json(500, {"error": "internal", "message": "服务内部错误"})

    def _dispatch(self, method: str) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        # normalize base
        if path.startswith("/bridge/v1"):
            path = path[len("/bridge/v1") :] or "/"
        if not path.startswith("/"):
            path = "/" + path

        if method == "GET" and path in ("/health", "/"):
            self._json(
                200,
                {
                    "ok": True,
                    "service": "aivia-bridge",
                    "mode": MODE,
                    "version": VERSION,
                    "host": HOST,
                    "exchange_token_required": bool(EXCHANGE_TOKEN),
                },
            )
            return

        if method == "POST" and path == "/auth/exchange":
            self._auth_exchange()
            return

        principal, err = self._principal()
        if not principal:
            msg = {
                "missing_token": "缺少身份令牌，请先登录或换票",
                "expired": "身份已过期，请重新登录",
                "invalid": "身份无效",
            }.get(err or "", "未授权")
            _audit({"op": "auth_fail", "path": path, "reason": err})
            self._json(401, {"error": "unauthorized", "message": msg})
            return

        if method == "GET" and path == "/me":
            self._json(
                200,
                {
                    "sub": principal["sub"],
                    "school_id": principal["school_id"],
                    "role": principal["role"],
                    "name": principal.get("name"),
                    "iss": principal.get("iss"),
                    "exp": principal.get("exp"),
                },
            )
            _audit({"op": "me", "sub": principal["sub"], "school_id": principal["school_id"]})
            return

        # /schools/{sid}/classes
        parts = [p for p in path.split("/") if p]
        if method == "GET" and len(parts) == 3 and parts[0] == "schools" and parts[2] == "classes":
            self._list_classes(principal, parts[1])
            return
        # /schools/{sid}/courses/{id}
        if method == "GET" and len(parts) == 4 and parts[0] == "schools" and parts[2] == "courses":
            self._get_course(principal, parts[1], parts[3])
            return

        if method == "POST" and path == "/proposals":
            self._create_proposal(principal)
            return
        if method == "GET" and path == "/proposals":
            self._list_proposals(principal)
            return
        if method == "POST" and len(parts) == 2 and parts[0] == "proposals" and parts[1] != "apply":
            # could be /proposals/{id}/review handled below
            pass
        if method == "POST" and len(parts) == 3 and parts[0] == "proposals" and parts[2] == "review":
            self._review_proposal(principal, parts[1])
            return
        if method == "POST" and len(parts) == 3 and parts[0] == "proposals" and parts[2] == "apply":
            _audit({"op": "apply_denied", "sub": principal["sub"]})
            self._json(
                403,
                {
                    "error": "forbidden",
                    "message": "Agent 与工具不得 apply 提案；仅人工流程可写 edu（本服务不暴露 apply）",
                },
            )
            return
        if method == "GET" and path == "/audit":
            self._list_audit(principal)
            return

        self._json(404, {"error": "not_found", "message": "接口不存在"})

    def _auth_exchange(self) -> None:
        if MODE != "mock":
            self._json(501, {"error": "not_implemented", "message": "real 模式换票后置"})
            return
        body = self._read_json()
        # F1: optional exchange gate
        if EXCHANGE_TOKEN:
            provided = (
                self.headers.get("X-Bridge-Exchange-Token")
                or body.get("exchange_token")
                or ""
            )
            if str(provided) != EXCHANGE_TOKEN:
                _audit({"op": "exchange_denied", "reason": "bad_exchange_token"})
                self._json(
                    401,
                    {
                        "error": "unauthorized",
                        "message": "mock 换票需要有效 X-Bridge-Exchange-Token（或 body.exchange_token）",
                    },
                )
                return
        sub = str(body.get("sub") or "t-demo")
        school_id = str(body.get("school_id") or "school-demo")
        role = str(body.get("role") or "teacher")
        name = str(body.get("name") or sub)
        if role not in ("teacher", "school_admin", "staff"):
            self._json(400, {"error": "bad_request", "message": "role 非法"})
            return
        token = issue_token(sub, school_id, role, name)
        _audit({"op": "exchange", "sub": sub, "school_id": school_id, "role": role})
        self._json(
            200,
            {
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": JWT_TTL,
                "principal": {"sub": sub, "school_id": school_id, "role": role, "name": name},
            },
        )

    def _require_school(self, principal: dict[str, Any], school_id: str) -> bool:
        if principal.get("school_id") != school_id:
            _audit(
                {
                    "op": "cross_school_denied",
                    "sub": principal.get("sub"),
                    "token_school": principal.get("school_id"),
                    "path_school": school_id,
                }
            )
            self._json(
                403,
                {
                    "error": "forbidden",
                    "message": "无权访问其他学校数据（租户隔离）",
                },
            )
            return False
        return True

    def _list_classes(self, principal: dict[str, Any], school_id: str) -> None:
        if not self._require_school(principal, school_id):
            return
        classes = MOCK_CLASSES.get(school_id, [])
        _audit({"op": "list_classes", "sub": principal["sub"], "school_id": school_id, "n": len(classes)})
        self._json(200, {"school_id": school_id, "classes": classes})

    def _get_course(self, principal: dict[str, Any], school_id: str, course_id: str) -> None:
        if not self._require_school(principal, school_id):
            return
        course = (MOCK_COURSES.get(school_id) or {}).get(course_id)
        if not course:
            self._json(404, {"error": "not_found", "message": "课程不存在或不在本校范围"})
            return
        _audit({"op": "get_course", "sub": principal["sub"], "school_id": school_id, "course_id": course_id})
        self._json(200, {"school_id": school_id, "course": course})

    def _create_proposal(self, principal: dict[str, Any]) -> None:
        body = self._read_json()
        ptype = str(body.get("type") or "lesson_plan_archive")
        title = str(body.get("title") or "未命名提案")
        # strip dangerous keys
        payload = {k: v for k, v in body.items() if k not in ("status", "apply", "id")}
        pid = str(uuid.uuid4())
        now = time.time()
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO proposals(id,school_id,author_sub,type,title,payload_json,status,created_at) VALUES(?,?,?,?,?,?,?,?)",
                (
                    pid,
                    principal["school_id"],
                    principal["sub"],
                    ptype,
                    title,
                    json.dumps(payload, ensure_ascii=False),
                    "pending_review",
                    now,
                ),
            )
            conn.commit()
        _audit({"op": "create_proposal", "sub": principal["sub"], "school_id": principal["school_id"], "id": pid})
        self._json(
            201,
            {
                "id": pid,
                "status": "pending_review",
                "school_id": principal["school_id"],
                "author_sub": principal["sub"],
                "type": ptype,
                "title": title,
                "message": "提案已创建，等待人审；AI 未写入 edu 业务库",
            },
        )

    def _list_proposals(self, principal: dict[str, Any]) -> None:
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(
                "SELECT id,school_id,author_sub,type,title,status,created_at,reviewed_by,review_note FROM proposals WHERE school_id=? ORDER BY created_at DESC LIMIT 100",
                (principal["school_id"],),
            ).fetchall()
        items = [
            {
                "id": r[0],
                "school_id": r[1],
                "author_sub": r[2],
                "type": r[3],
                "title": r[4],
                "status": r[5],
                "created_at": r[6],
                "reviewed_by": r[7],
                "review_note": r[8],
            }
            for r in rows
        ]
        self._json(200, {"proposals": items})

    def _review_proposal(self, principal: dict[str, Any], pid: str) -> None:
        if principal.get("role") != "school_admin":
            self._json(403, {"error": "forbidden", "message": "仅 school_admin 可人审提案"})
            return
        body = self._read_json()
        decision = str(body.get("decision") or body.get("status") or "").lower()
        note = str(body.get("note") or "")
        if decision in ("approve", "approved"):
            status = "approved"
        elif decision in ("reject", "rejected"):
            status = "rejected"
        else:
            self._json(400, {"error": "bad_request", "message": "decision 须为 approved 或 rejected"})
            return
        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute("SELECT school_id,status FROM proposals WHERE id=?", (pid,)).fetchone()
            if not row:
                self._json(404, {"error": "not_found", "message": "提案不存在"})
                return
            if row[0] != principal["school_id"]:
                self._json(403, {"error": "forbidden", "message": "跨校提案不可审"})
                return
            conn.execute(
                "UPDATE proposals SET status=?, reviewed_by=?, review_note=?, reviewed_at=? WHERE id=?",
                (status, principal["sub"], note, time.time(), pid),
            )
            conn.commit()
        _audit(
            {
                "op": "review_proposal",
                "sub": principal["sub"],
                "id": pid,
                "status": status,
            }
        )
        self._json(
            200,
            {
                "id": pid,
                "status": status,
                "message": "人审完成；仍未自动写入 edu 业务库（无 Agent apply）",
            },
        )

    def _list_audit(self, principal: dict[str, Any]) -> None:
        if principal.get("role") != "school_admin":
            self._json(403, {"error": "forbidden", "message": "仅 school_admin 可查审计"})
            return
        lines: list[dict[str, Any]] = []
        if AUDIT_PATH.exists():
            for line in AUDIT_PATH.read_text(encoding="utf-8").splitlines()[-200:]:
                try:
                    lines.append(json.loads(line))
                except Exception:
                    continue
        # F4: default only same school_id (+ exchange/auth events tagged with school)
        sid = principal["school_id"]
        filtered = []
        for x in lines:
            ev_sid = x.get("school_id") or x.get("token_school") or x.get("path_school")
            if ev_sid is None:
                # keep global infra events only if op is exchange/auth for this school later
                if x.get("op") in ("exchange", "exchange_denied", "auth_fail") and x.get("school_id") in (None, sid):
                    if x.get("school_id") in (None, sid):
                        filtered.append(x)
                continue
            if ev_sid == sid:
                filtered.append(x)
        self._json(200, {"school_id": sid, "events": filtered[-50:]})


def main() -> None:
    require_strong_secret()
    _ensure_db()
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(
        f"[aivia-bridge] v{VERSION} MODE={MODE} listen http://{HOST}:{PORT}/bridge/v1/health "
        f"exchange_token={'on' if EXCHANGE_TOKEN else 'off'}",
        flush=True,
    )
    httpd.serve_forever()


if __name__ == "__main__":
    main()
