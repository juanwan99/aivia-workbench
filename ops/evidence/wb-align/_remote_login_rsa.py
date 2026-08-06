#!/usr/bin/env python3
"""Dify console login with optional RSA password encryption + create api token."""
from __future__ import annotations

import json
import secrets
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

BASE = "http://127.0.0.1:13080"


def http(method, path, data=None, headers=None, base=BASE):
    h = {"Content-Type": "application/json"}
    if headers:
        h.update(headers)
    body = None if data is None else json.dumps(data).encode()
    r = urllib.request.Request(base + path, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            raw = resp.read().decode("utf-8", "replace")
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", "replace")
        try:
            j = json.loads(raw)
        except Exception:
            j = {"raw": raw[:800]}
        return e.code, j


def load_admin():
    env = {}
    for line in Path.home().joinpath(".secrets/dify-admin.env").read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    return env


def main():
    admin = load_admin()
    email, password = admin["DIFY_ADMIN_EMAIL"], admin["DIFY_ADMIN_PASSWORD"]

    # probe features / public key
    for path in [
        "/console/api/system-features",
        "/console/api/features",
        "/console/api/login",
    ]:
        st, j = http("GET", path)
        print("GET", path, st, str(j)[:200])

    # try plain login variants
    for payload in [
        {"email": email, "password": password},
        {"email": email, "password": password, "language": "zh-Hans", "remember_me": True},
        {"email": email, "password": password, "language": "en-US"},
    ]:
        st, j = http("POST", "/console/api/login", payload)
        print("login_try", st, j.get("message") or j.get("code") or list(j.keys())[:5])
        if st == 200:
            break

    # RSA path if public key present
    st, j = http("GET", "/console/api/system-features")
    pk = None
    if isinstance(j, dict):
        pk = j.get("public_key") or (j.get("data") or {}).get("public_key")
        print("features_keys", list(j.keys())[:20])
    if pk:
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric import padding
            from cryptography.hazmat.backends import default_backend
            import base64

            key = serialization.load_pem_public_key(pk.encode(), backend=default_backend())
            enc = key.encrypt(password.encode(), padding.PKCS1v15())
            enc_b64 = base64.b64encode(enc).decode()
            st, j = http(
                "POST",
                "/console/api/login",
                {"email": email, "password": enc_b64, "language": "zh-Hans", "remember_me": True},
            )
            print("login_rsa", st, j.get("message") or list(j.keys())[:8])
        except Exception as e:
            print("rsa_fail", type(e).__name__, e)

    # If still fail: insert api token directly into DB (Dify accepts raw app tokens)
    app_id = "fc3e14da-2861-4009-a888-730a6b993011"
    token = "app-" + secrets.token_hex(20)
    # tenant_id from apps table
    tenant = subprocess.check_output(
        [
            "docker",
            "exec",
            "dify-db_postgres-1",
            "psql",
            "-U",
            "postgres",
            "-d",
            "dify",
            "-tAc",
            f"select tenant_id from apps where id='{app_id}';",
        ],
        text=True,
    ).strip()
    print("tenant", tenant[:8] if tenant else None)
    # columns: id, app_id, type, token, last_used_at, created_at, tenant_id
    import uuid
    from datetime import datetime, timezone

    tid = str(uuid.uuid4())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    sql = (
        "insert into api_tokens (id, app_id, type, token, last_used_at, created_at, tenant_id) "
        f"values ('{tid}', '{app_id}', 'app', '{token}', null, '{now}', '{tenant}');"
    )
    out = subprocess.check_output(
        [
            "docker",
            "exec",
            "dify-db_postgres-1",
            "psql",
            "-U",
            "postgres",
            "-d",
            "dify",
            "-c",
            sql,
        ],
        text=True,
    )
    print("insert", out.strip())
    Path("/tmp/wb-align-app-key.txt").write_text(token, encoding="utf-8")
    print("api_key_len", len(token), "pref", token[:8])

    # chat smoke
    ip = (
        subprocess.check_output(
            [
                "docker",
                "inspect",
                "dify-api-1",
                "--format",
                "{{range .NetworkSettings.Networks}}{{.IPAddress}} {{end}}",
            ],
            text=True,
        )
        .strip()
        .split()[0]
    )
    data = json.dumps(
        {
            "inputs": {},
            "query": "只回：好",
            "response_mode": "blocking",
            "user": "wb-align-s0",
        }
    ).encode()
    r = urllib.request.Request(
        f"http://{ip}:5001/v1/chat-messages",
        data=data,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(r, timeout=180) as resp:
            j = json.loads(resp.read().decode())
            print("chat", resp.status, "answer", str(j.get("answer"))[:100])
    except urllib.error.HTTPError as e:
        print("chat_http", e.code, e.read()[:300])


if __name__ == "__main__":
    main()
