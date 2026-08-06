# aivia-bridge

MODE: **hybrid** (v0.2.2) — fixture catalog + exchange gate + **public file download store** + **ops metrics**.  
Not full real until edu-core only-read APIs exist.

## Download path (PHASE-DL-FIX)

| Endpoint | Auth | Purpose |
|----------|------|---------|
| `POST /dl/put` | `X-Aivia-Dl-Put` = `BRIDGE_DL_PUT_TOKEN` | Sandbox Code node uploads blob |
| `GET /dl/{id}/file.{ext}` | public | Browser download (via `https://workbench.aivia.asia/dl/...`) |

## Ops (PHASE-WB-ALIGN S1)

| Endpoint | Auth | Purpose |
|----------|------|---------|
| `GET /ops/metrics` | `X-Aivia-Ops` (or put token) | G-07/G-13 counters + daily put usage |
| `GET /ops/audit/tail?n=50` | ops token | G-03 audit sample |
| `GET /ops/policy` | ops token | G-05 write-deny policy JSON |
| `POST /ops/quality-event` | ops token | record `empty_success` / `fail` / `refuse_write` |

Env: `BRIDGE_DL_DAILY_MAX` (default 200), `BRIDGE_OPS_TOKEN` (optional; falls back to put token).

Env (secrets only, never commit):

- `BRIDGE_DL_PUT_TOKEN` — put gate  
- `BRIDGE_PUBLIC_DL_BASE` — default `https://workbench.aivia.asia/dl`  
- `BRIDGE_DL_DIR` — default `$BRIDGE_DATA_DIR/public-dl`

## Run

```bash
# host smoke
bash bridge/run.sh
bash bridge/smoke.sh
```

Docker (Dify sandbox reachability): container `aivia-bridge` on `dify_default`.

## Safety

- `BRIDGE_EXCHANGE_TOKEN` required for hybrid
- No agent `/apply`
- Secrets in `~/.secrets/bridge.env` only
- Put token never logged in audit payload values