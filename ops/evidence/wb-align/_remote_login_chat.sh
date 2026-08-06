#!/bin/bash
# Login Dify console, get app API key, run S0 chat regressions — never echo secrets
set -euo pipefail
BASE="http://127.0.0.1:13080"
python3 - <<'PY'
from pathlib import Path
import json, urllib.request, urllib.error, ssl, os, re, time

base = "http://127.0.0.1:13080"
admin = {}
for line in Path.home().joinpath(".secrets/dify-admin.env").read_text(encoding="utf-8").splitlines():
    if "=" in line and not line.strip().startswith("#"):
        k,v=line.split("=",1); admin[k.strip()]=v.strip().strip('"').strip("'")

email = admin.get("DIFY_ADMIN_EMAIL")
password = admin.get("DIFY_ADMIN_PASSWORD")
assert email and password, "missing admin"

def req(method, path, data=None, token=None):
    headers={"Content-Type":"application/json"}
    if token:
        headers["Authorization"]=f"Bearer {token}"
    body=None if data is None else json.dumps(data).encode()
    r=urllib.request.Request(base+path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            raw=resp.read().decode("utf-8","replace")
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw=e.read().decode("utf-8","replace")
        try:
            j=json.loads(raw)
        except Exception:
            j={"raw":raw[:500]}
        return e.code, j

# login
st, j = req("POST", "/console/api/login", {"email": email, "password": password})
print("login", st, list(j.keys())[:10])
token = j.get("data",{}).get("access_token") or j.get("access_token") or j.get("result")
if isinstance(j.get("data"), dict):
    token = j["data"].get("access_token") or j["data"].get("token") or token
# sometimes nested
if not token and "data" in j:
    print("login_data_keys", j.get("data"))
assert token, f"no token: {str(j)[:300]}"
print("token_len", len(token))

# list apps
st, j = req("GET", "/console/api/apps?page=1&limit=50", token=token)
print("apps", st)
apps = j.get("data") or []
for a in apps:
    site=a.get("site") or {}
    print("-", a.get("name"), a.get("mode"), "id", a.get("id"), "site_code", site.get("code") or site.get("access_token"))

# prefer chatflow / advanced-chat app named scene or 课件
target=None
for a in apps:
    name=(a.get("name") or "")
    if "scene" in name.lower() or "课件" in name or a.get("mode") in ("advanced-chat","chat"):
        target=a
if not target and apps:
    target=apps[0]
print("target", target.get("name") if target else None, target.get("id") if target else None)
app_id=target["id"]

# get or create api key
st, j = req("GET", f"/console/api/apps/{app_id}/api-keys", token=token)
print("list_keys", st, j if st!=200 else f"n={len(j.get('data') or j if isinstance(j,list) else [])}")
keys = j.get("data") if isinstance(j, dict) else j
api_key=None
if isinstance(keys, list) and keys:
    api_key = keys[0].get("token") or keys[0].get("key")
if not api_key:
    st, j = req("POST", f"/console/api/apps/{app_id}/api-keys", {}, token=token)
    print("create_key", st, list(j.keys()) if isinstance(j,dict) else type(j))
    api_key = (j.get("token") or j.get("key") or (j.get("data") or {}).get("token"))
print("api_key_len", len(api_key or ""))
assert api_key, "no api key"

# save to temp only on server (not git)
Path("/tmp/wb-align-app-key.txt").write_text(api_key, encoding="utf-8")
Path("/tmp/wb-align-app-id.txt").write_text(app_id, encoding="utf-8")
print("saved /tmp/wb-align-app-key.txt")

# chat via api container network using urllib to api IP
import socket
# discover api host via docker DNS from host? use 127.0.0.1:13080 might not proxy /v1
# try through nginx reverse?
for chat_base in [
    "http://127.0.0.1:13080/v1",
    "http://172.22.0.13:5001/v1",
]:
    try:
        data=json.dumps({"inputs":{},"query":"只回：好","response_mode":"blocking","user":"wb-align-s0"}).encode()
        r=urllib.request.Request(chat_base+"/chat-messages", data=data, headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type":"application/json",
        }, method="POST")
        with urllib.request.urlopen(r, timeout=120) as resp:
            raw=resp.read().decode()
            d=json.loads(raw)
            print("chat_ok", chat_base, "answer", str(d.get("answer",""))[:80])
            Path("/tmp/wb-align-chat-base.txt").write_text(chat_base, encoding="utf-8")
            break
    except Exception as e:
        print("chat_fail", chat_base, type(e).__name__, e)
PY
