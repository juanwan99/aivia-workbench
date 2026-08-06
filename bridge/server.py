#!/usr/bin/env python3
"""Aivia edu-bridge — identity, read-only, proposals, audit.

MODE:
  mock    — in-memory demo catalog (CLAIM-C)
  hybrid  — fixture catalog (true structure, not live edu API) + exchange gate
  real    — live edu-core only-read (exchange still gate; live paths later)

Hard rules:
  - No AI write path to edu business DB
  - No /apply for agents
  - school_id isolation
  - Never bind public anonymous exchange
"""
from __future__ import annotations

import base64
import json
import os
import re
import sqlite3
import threading
import time
import traceback
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, unquote, urlparse

import jwt

VERSION = "0.2.1"
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

MODE = os.environ.get("BRIDGE_MODE", "mock").strip().lower()
HOST = os.environ.get("BRIDGE_HOST", "127.0.0.1")
# comma-separated extra bind addresses (e.g. docker host gateway 172.22.0.1)
EXTRA_HOSTS = [
    h.strip()
    for h in os.environ.get("BRIDGE_EXTRA_HOSTS", "").split(",")
    if h.strip() and h.strip() != HOST
]
PORT = int(os.environ.get("BRIDGE_PORT", "18090"))
JWT_SECRET = os.environ.get("BRIDGE_JWT_SECRET", "")
_DEFAULT_ISS = {
    "mock": "bridge-mock",
    "hybrid": "bridge-hybrid",
    "real": "bridge-real",
}.get(MODE, "bridge-mock")
JWT_ISS = os.environ.get("BRIDGE_JWT_ISS", _DEFAULT_ISS)
JWT_TTL = int(os.environ.get("BRIDGE_JWT_TTL", "3600"))
# Gate for /auth/exchange (header X-Bridge-Exchange-Token or body exchange_token)
EXCHANGE_TOKEN = os.environ.get("BRIDGE_EXCHANGE_TOKEN", "").strip()
# Gate for public Chat file put (sandbox → bridge). Never commit real value.
DL_PUT_TOKEN = os.environ.get("BRIDGE_DL_PUT_TOKEN", "").strip()
# Public base for download links shown in Chat (HTTPS on workbench)
PUBLIC_DL_BASE = os.environ.get(
    "BRIDGE_PUBLIC_DL_BASE", "https://workbench.aivia.asia/dl"
).rstrip("/")
DL_MAX_BYTES = int(os.environ.get("BRIDGE_DL_MAX_BYTES", str(3 * 1024 * 1024)))
DATA_DIR = Path(os.environ.get("BRIDGE_DATA_DIR", str(Path(__file__).resolve().parent / "data")))
DB_PATH = DATA_DIR / "bridge.sqlite3"
AUDIT_PATH = DATA_DIR / "audit.jsonl"
DL_DIR = Path(os.environ.get("BRIDGE_DL_DIR", str(DATA_DIR / "public-dl")))
FIXTURE_PATH = Path(
    os.environ.get(
        "BRIDGE_HYBRID_FIXTURE",
        str(Path(__file__).resolve().parent / "data" / "hybrid-fixture.json"),
    )
)


def require_strong_secret() -> None:
    """F1: refuse to start with missing/weak JWT secret."""
    if MODE not in ("mock", "hybrid", "real"):
        raise SystemExit(f"[aivia-bridge] FATAL: BRIDGE_MODE invalid: {MODE!r}")
    if not JWT_SECRET or JWT_SECRET in WEAK_SECRETS or len(JWT_SECRET) < 24:
        raise SystemExit(
            "[aivia-bridge] FATAL: BRIDGE_JWT_SECRET missing or weak. "
            "Set a long random value in ~/.secrets/bridge.env (never commit)."
        )
    binds = [HOST, *EXTRA_HOSTS]
    non_loop = [h for h in binds if h not in ("127.0.0.1", "localhost", "::1")]
    if non_loop and not EXCHANGE_TOKEN:
        raise SystemExit(
            "[aivia-bridge] FATAL: non-loopback bind requires BRIDGE_EXCHANGE_TOKEN "
            f"(binds={binds}). Refusing open exchange on network peers."
        )
    if MODE in ("hybrid", "real") and not EXCHANGE_TOKEN:
        raise SystemExit(
            f"[aivia-bridge] FATAL: MODE={MODE} requires BRIDGE_EXCHANGE_TOKEN (no anonymous exchange)."
        )


# Built-in mock catalog
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


def _load_catalog() -> tuple[dict[str, list], dict[str, dict]]:
    """Return (classes_by_school, courses_by_school). hybrid uses fixture file."""
    if MODE == "mock":
        return MOCK_CLASSES, MOCK_COURSES
    if MODE == "hybrid":
        if not FIXTURE_PATH.exists():
            raise SystemExit(f"[aivia-bridge] FATAL: hybrid fixture missing: {FIXTURE_PATH}")
        data = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        classes = data.get("classes") or {}
        courses = data.get("courses") or {}
        if not classes or not courses:
            raise SystemExit("[aivia-bridge] FATAL: hybrid fixture empty classes/courses")
        return classes, courses
    # real: live edu not wired yet — refuse silent full-real claim
    raise SystemExit(
        "[aivia-bridge] FATAL: MODE=real requires live edu-core only-read adapter "
        "(not implemented). Use hybrid until edu API is ready."
    )


CLASSES_BY_SCHOOL, COURSES_BY_SCHOOL = ({}, {})  # filled in main after require

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
        if getattr(self, "_aivia_body_started", False):
            return
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self._aivia_body_started = True
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Bridge-Mode", MODE)
        self.send_header("Connection", "close")
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
            try:
                _audit({"level": "error", "err": str(e), "path": self.path})
            except Exception:
                pass
            # Never append JSON after a partial file response (causes nginx 502)
            if not getattr(self, "_headers_buffer", None) and not getattr(
                self, "wfile", None
            ):
                return
            try:
                if not self.headers_sent if hasattr(self, "headers_sent") else False:
                    pass
            except Exception:
                pass
            # BaseHTTPRequestHandler has no headers_sent flag on all versions; use guard
            if getattr(self, "_aivia_body_started", False):
                return
            try:
                self._json(500, {"error": "internal", "message": "服务内部错误"})
            except Exception:
                return

    def do_POST(self) -> None:  # noqa: N802
        try:
            self._dispatch("POST")
        except Exception as e:
            try:
                _audit(
                    {
                        "level": "error",
                        "err": str(e),
                        "path": self.path,
                        "tb": traceback.format_exc()[-500:],
                    }
                )
            except Exception:
                pass
            if getattr(self, "_aivia_body_started", False):
                return
            try:
                self._json(500, {"error": "internal", "message": "服务内部错误"})
            except Exception:
                return

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
                    "dl_put_enabled": bool(DL_PUT_TOKEN) and len(DL_PUT_TOKEN) >= 16,
                    "public_dl_base": PUBLIC_DL_BASE,
                },
            )
            return

        if method == "POST" and path == "/auth/exchange":
            self._auth_exchange()
            return

        # ---- public download store (PHASE-DL-FIX): no JWT ----
        # PUT is gated by BRIDGE_DL_PUT_TOKEN (sandbox code node).
        # GET is public unguessable /dl/{id}/{filename}.
        if method == "POST" and path == "/dl/put":
            self._dl_put()
            return
        if method == "GET" and path.startswith("/dl/"):
            self._dl_get(path)
            return
        if method == "GET" and path == "/dl":
            self._json(400, {"error": "bad_request", "message": "需要 /dl/{id}/{filename}"})
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

    def _safe_filename(self, name: str) -> str:
        base = Path(name or "file.bin").name
        base = re.sub(r"[^\w\u4e00-\u9fff.\-]+", "_", base).strip("._") or "file.bin"
        return base[:120]

    def _dl_put(self) -> None:
        """Store a file for public HTTPS download (Chat PackDownload path)."""
        if not DL_PUT_TOKEN or len(DL_PUT_TOKEN) < 16:
            self._json(503, {"error": "dl_disabled", "message": "下载落盘未配置 BRIDGE_DL_PUT_TOKEN"})
            return
        got = (self.headers.get("X-Aivia-Dl-Put") or self.headers.get("X-Dl-Put-Token") or "").strip()
        if got != DL_PUT_TOKEN:
            _audit({"op": "dl_put_denied", "reason": "bad_token"})
            self._json(401, {"error": "unauthorized", "message": "无效的上传令牌"})
            return
        body = self._read_json()
        filename = self._safe_filename(str(body.get("filename") or "file.bin"))
        mime = str(body.get("mime") or "application/octet-stream")[:120]
        b64 = body.get("content_b64") or body.get("b64") or ""
        if not isinstance(b64, str) or not b64.strip():
            self._json(400, {"error": "bad_request", "message": "缺少 content_b64"})
            return
        try:
            raw = base64.b64decode(b64, validate=False)
        except Exception:
            self._json(400, {"error": "bad_request", "message": "content_b64 无效"})
            return
        if len(raw) <= 0:
            self._json(400, {"error": "bad_request", "message": "空文件"})
            return
        if len(raw) > DL_MAX_BYTES:
            self._json(
                413,
                {
                    "error": "too_large",
                    "message": f"文件超过上限 {DL_MAX_BYTES} 字节",
                    "size": len(raw),
                },
            )
            return
        file_id = uuid.uuid4().hex
        dest_dir = DL_DIR / file_id
        dest_dir.mkdir(parents=True, exist_ok=True)
        # ASCII-only store name + URL (Chinese/real name only in Content-Disposition)
        ext = Path(filename).suffix.lower()
        if not re.fullmatch(r"\.[a-z0-9]{1,10}", ext or ""):
            ext = ".bin"
        store_name = f"file{ext}"
        dest = dest_dir / store_name
        dest.write_bytes(raw)
        (dest_dir / ".meta.json").write_text(
            json.dumps(
                {
                    "filename": filename,
                    "store_name": store_name,
                    "mime": mime,
                    "size": len(raw),
                    "created_at": time.time(),
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        url = f"{PUBLIC_DL_BASE}/{file_id}/{store_name}"
        try:
            _audit(
                {
                    "op": "dl_put",
                    "file_id": file_id,
                    "filename": filename,
                    "size": len(raw),
                    "mime": mime,
                }
            )
        except Exception:
            pass
        self._json(
            200,
            {
                "ok": True,
                "id": file_id,
                "filename": filename,
                "mime": mime,
                "size": len(raw),
                "url": url,
            },
        )

    def _dl_get(self, path: str) -> None:
        """Public GET /dl/{id}/file.ext — ASCII path; real name via Content-Disposition."""
        parts = [p for p in path.split("/") if p]
        # ["dl", id] or ["dl", id, store_name]
        if len(parts) < 2 or parts[0] != "dl":
            self._json(404, {"error": "not_found", "message": "文件不存在"})
            return
        file_id = parts[1]
        if not re.fullmatch(r"[0-9a-f]{32}", file_id):
            self._json(404, {"error": "not_found", "message": "文件不存在"})
            return
        dest_dir = DL_DIR / file_id
        meta_path = dest_dir / ".meta.json"
        meta: dict[str, Any] = {}
        if meta_path.is_file():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except Exception:
                meta = {}
        store_name = str(meta.get("store_name") or "")
        if len(parts) >= 3:
            cand = Path(parts[2]).name
            if re.fullmatch(r"file\.[a-z0-9]{1,10}", cand):
                store_name = cand
        if not store_name:
            cands = [p for p in dest_dir.iterdir() if p.is_file() and p.name != ".meta.json"] if dest_dir.is_dir() else []
            if len(cands) == 1:
                store_name = cands[0].name
            else:
                self._json(404, {"error": "not_found", "message": "文件不存在"})
                return
        dest = dest_dir / store_name
        if not dest.is_file():
            self._json(404, {"error": "not_found", "message": "文件不存在"})
            return
        filename = self._safe_filename(str(meta.get("filename") or store_name))
        mime = str(meta.get("mime") or "application/octet-stream")
        data = dest.read_bytes()
        # ASCII fallback filename for old clients + RFC 5987
        ascii_fb = store_name if re.fullmatch(r"[\w.\-]+", store_name) else "download.bin"
        cd = f"attachment; filename=\"{ascii_fb}\"; filename*=UTF-8''{quote(filename)}"
        try:
            self._aivia_body_started = True
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Content-Disposition", cd)
            self.send_header("Cache-Control", "private, max-age=3600")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Bridge-Mode", MODE)
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(data)
        except BrokenPipeError:
            return
        try:
            _audit({"op": "dl_get", "file_id": file_id, "filename": filename, "size": len(data)})
        except Exception:
            pass

    def _auth_exchange(self) -> None:
        # mock + hybrid: gated exchange (pilot IdP stand-in). real: not open.
        if MODE == "real":
            self._json(
                501,
                {
                    "error": "not_implemented",
                    "message": "MODE=real 须接 edu IdP/JWT 校验；禁止开放 exchange 冒充 full real",
                },
            )
            return
        body = self._read_json()
        # hybrid always requires token; mock requires when configured
        need_gate = bool(EXCHANGE_TOKEN) or MODE == "hybrid"
        if need_gate:
            provided = (
                self.headers.get("X-Bridge-Exchange-Token")
                or body.get("exchange_token")
                or ""
            )
            if not EXCHANGE_TOKEN or str(provided) != EXCHANGE_TOKEN:
                _audit({"op": "exchange_denied", "reason": "bad_exchange_token", "mode": MODE})
                self._json(
                    401,
                    {
                        "error": "unauthorized",
                        "message": f"{MODE} 换票需要有效 X-Bridge-Exchange-Token（或 body.exchange_token）",
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
        _audit({"op": "exchange", "sub": sub, "school_id": school_id, "role": role, "mode": MODE})
        self._json(
            200,
            {
                "access_token": token,
                "token_type": "Bearer",
                "expires_in": JWT_TTL,
                "mode": MODE,
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
        classes = CLASSES_BY_SCHOOL.get(school_id, [])
        _audit(
            {
                "op": "list_classes",
                "sub": principal["sub"],
                "school_id": school_id,
                "n": len(classes),
                "source": "fixture" if MODE == "hybrid" else MODE,
            }
        )
        self._json(
            200,
            {
                "school_id": school_id,
                "classes": classes,
                "source": "hybrid-fixture" if MODE == "hybrid" else MODE,
            },
        )

    def _get_course(self, principal: dict[str, Any], school_id: str, course_id: str) -> None:
        if not self._require_school(principal, school_id):
            return
        course = (COURSES_BY_SCHOOL.get(school_id) or {}).get(course_id)
        if not course:
            self._json(404, {"error": "not_found", "message": "课程不存在或不在本校范围"})
            return
        _audit(
            {
                "op": "get_course",
                "sub": principal["sub"],
                "school_id": school_id,
                "course_id": course_id,
                "source": "fixture" if MODE == "hybrid" else MODE,
            }
        )
        self._json(
            200,
            {
                "school_id": school_id,
                "course": course,
                "source": "hybrid-fixture" if MODE == "hybrid" else MODE,
            },
        )

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
    global CLASSES_BY_SCHOOL, COURSES_BY_SCHOOL
    require_strong_secret()
    CLASSES_BY_SCHOOL, COURSES_BY_SCHOOL = _load_catalog()
    _ensure_db()
    # re-read extra hosts at runtime (import-time may miss env race)
    extra = [
        h.strip()
        for h in os.environ.get("BRIDGE_EXTRA_HOSTS", "").split(",")
        if h.strip() and h.strip() != HOST
    ]
    binds = [HOST, *extra]
    print(f"[aivia-bridge] binds={binds} MODE={MODE}", flush=True)
    servers: list[ThreadingHTTPServer] = []
    for h in binds:
        try:
            ThreadingHTTPServer.allow_reuse_address = True
            httpd = ThreadingHTTPServer((h, PORT), Handler)
        except OSError as e:
            print(f"[aivia-bridge] FATAL bind {h}:{PORT}: {e}", flush=True)
            raise
        servers.append(httpd)
        t = threading.Thread(target=httpd.serve_forever, name=f"bridge-{h}", daemon=True)
        t.start()
        print(
            f"[aivia-bridge] v{VERSION} MODE={MODE} listen http://{h}:{PORT}/bridge/v1/health "
            f"exchange_token={'on' if EXCHANGE_TOKEN else 'off'} iss={JWT_ISS}",
            flush=True,
        )
    # keep main thread alive
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        for s in servers:
            s.shutdown()


if __name__ == "__main__":
    main()
