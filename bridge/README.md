# aivia-bridge

MODE: **hybrid** (v0.2.1) — fixture catalog + exchange gate + **public file download store**.  
Not full real until edu-core only-read APIs exist.

## Download path (PHASE-DL-FIX)

| Endpoint | Auth | Purpose |
|----------|------|---------|
| `POST /dl/put` | `X-Aivia-Dl-Put` = `BRIDGE_DL_PUT_TOKEN` | Sandbox Code node uploads blob |
| `GET /dl/{id}/file.{ext}` | public | Browser download (via `https://workbench.aivia.asia/dl/...`) |

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