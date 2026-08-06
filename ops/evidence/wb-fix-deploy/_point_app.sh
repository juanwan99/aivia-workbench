#!/bin/bash
set -e
NEW=$(cat /tmp/wb-fix-new-wf-id.txt)
echo "NEW=$NEW"
docker exec dify-db_postgres-1 psql -U postgres -d dify -c "select id,name,workflow_id from apps;"
docker exec dify-db_postgres-1 psql -U postgres -d dify -c "update apps set workflow_id='$NEW', updated_at=now() where id='fc3e14da-2861-4009-a888-730a6b993011';"
docker exec dify-db_postgres-1 psql -U postgres -d dify -c "select id,name,workflow_id from apps where id='fc3e14da-2861-4009-a888-730a6b993011';"
# flush redis cache if any
docker exec dify-redis-1 redis-cli FLUSHDB 2>/dev/null || true
echo "api_tokens=$(docker exec dify-db_postgres-1 psql -U postgres -d dify -tAc "select count(*) from api_tokens where app_id='fc3e14da-2861-4009-a888-730a6b993011';")"
test -f /tmp/wb-align-app-key.txt && echo has_key || echo no_key
echo DONE
