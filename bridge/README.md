# aivia-bridge

MODE: **hybrid** (v0.2.0) — fixture catalog + exchange gate.  
Not full real until edu-core only-read APIs exist.

## Run

```bash
# host smoke
bash bridge/run.sh
bash bridge/smoke.sh
```

Docker (Dify reachability): container `aivia-bridge` on `dify_default`.

## Safety

- `BRIDGE_EXCHANGE_TOKEN` required for hybrid
- No agent `/apply`
- Secrets in `~/.secrets/bridge.env` only
