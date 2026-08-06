#!/usr/bin/env python3
"""Login Dify console, ensure app API key, smoke chat. Secrets never printed."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path

BASE = "http://127.0.0.1:13080"


def load_env(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def req(method: str, path: str, data=None, token: str | None = None, base: str = BASE):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    body = None if data is None else json.dumps(data).encode()
    r = urllib.request.Request(base + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=180) as resp:
            raw = resp.read().decode("utf-8", "replace")
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            j = json.loads(raw)
        except Exception:
            j = {"raw": raw[:800]}
        return e.code, j


def main() -> None:
    admin = load_env(Path.home() / ".secrets" / "dify-admin.env")
    email = admin["DIFY_ADMIN_EMAIL"]
    password = admin["DIFY_ADMIN_PASSWORD"]

    st, j = req("POST", "/console/api/login", {"email": email, "password": password})
    print("login", st, sorted(j.keys())[:12])
    data = j.get("data") if isinstance(j.get("data"), dict) else j
    token = None
    if isinstance(data, dict):
        token = data.get("access_token") or data.get("token")
    token = token or j.get("access_token")
    if not token:
        # some versions wrap differently
        print("login_body_sample", str(j)[:400])
        raise SystemExit("no token")
    print("token_len", len(token))

    st, j = req("GET", "/console/api/apps?page=1&limit=50", token=token)
    print("apps", st)
    apps = j.get("data") or []
    for a in apps:
        site = a.get("site") or {}
        print(
            "-",
            a.get("name"),
            a.get("mode"),
            "id",
            a.get("id"),
            "code",
            site.get("code"),
        )

    target = None
    for a in apps:
        name = (a.get("name") or "").lower()
        if "scene" in name or "课件" in (a.get("name") or "") or a.get("mode") in (
            "advanced-chat",
            "chat",
            "agent-chat",
        ):
            target = a
            if "scene" in name or "lOMV" in str(site := a.get("site") or {}):
                break
    # prefer site code match from PIN
    for a in apps:
        site = a.get("site") or {}
        if site.get("code") == "lOMVPbz7rZmbJSJl":
            target = a
            break
    if not target and apps:
        target = apps[0]
    print("target", target.get("name"), target.get("id"))
    app_id = target["id"]

    st, j = req("GET", f"/console/api/apps/{app_id}/api-keys", token=token)
    print("list_keys", st)
    keys = j.get("data") if isinstance(j, dict) else j
    api_key = None
    if isinstance(keys, list) and keys:
        api_key = keys[0].get("token") or keys[0].get("key")
    if not api_key:
        st, j = req("POST", f"/console/api/apps/{app_id}/api-keys", {}, token=token)
        print("create_key", st, sorted(j.keys()) if isinstance(j, dict) else type(j))
        api_key = j.get("token") or j.get("key")
        if isinstance(j.get("data"), dict):
            api_key = api_key or j["data"].get("token") or j["data"].get("key")
    if not api_key:
        print("keys_body", str(j)[:400])
        raise SystemExit("no api key")
    print("api_key_len", len(api_key))
    Path("/tmp/wb-align-app-key.txt").write_text(api_key, encoding="utf-8")
    Path("/tmp/wb-align-app-id.txt").write_text(app_id, encoding="utf-8")
    Path("/tmp/wb-align-console-token.txt").write_text(token, encoding="utf-8")

    # chat bases to try
    chat_bases = [
        "http://127.0.0.1:13080/v1",
        "http://172.22.0.13:5001/v1",
        "http://172.24.0.8:5001/v1",
    ]
    ok = False
    for chat_base in chat_bases:
        try:
            st, j = req(
                "POST",
                "/chat-messages",
                {
                    "inputs": {},
                    "query": "只回：好",
                    "response_mode": "blocking",
                    "user": "wb-align-s0",
                },
                token=api_key,
                base=chat_base,
            )
            print("chat", chat_base, st, "answer", str(j.get("answer", j))[:120])
            if st == 200 and j.get("answer") is not None:
                Path("/tmp/wb-align-chat-base.txt").write_text(chat_base, encoding="utf-8")
                ok = True
                break
        except Exception as e:
            print("chat_exc", chat_base, type(e).__name__, e)
    if not ok:
        raise SystemExit("chat failed all bases")
    print("DONE")


if __name__ == "__main__":
    main()
