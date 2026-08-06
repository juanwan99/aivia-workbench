#!/usr/bin/env python3
"""Inspect Dify app config tables for PackDownload / prompts (no secrets printed)."""
import subprocess

def psql(sql: str) -> str:
    return subprocess.check_output(
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
        stderr=subprocess.STDOUT,
    )

app_id = "fc3e14da-2861-4009-a888-730a6b993011"
print("=== apps ===")
print(psql("select id,name,mode,status from apps;"))
print("=== tables like workflow/app_model ===")
print(psql("select tablename from pg_tables where schemaname='public' and (tablename like '%workflow%' or tablename like '%app_model%' or tablename like '%site%') order by 1;"))
print("=== app_model_configs columns ===")
print(psql("select column_name from information_schema.columns where table_name='app_model_configs' order by ordinal_position;"))
print("=== workflows for app ===")
print(psql(f"select id, version, marked_name, created_at from workflows where app_id='{app_id}' order by created_at desc limit 5;"))
print("=== sites ===")
print(psql(f"select app_id, code, title, status from sites where app_id='{app_id}';"))
# peek pre_prompt length
print("=== pre_prompt head ===")
print(psql(f"select length(pre_prompt), left(pre_prompt,400) from app_model_configs where app_id='{app_id}' order by updated_at desc nulls last limit 1;"))
print("=== suggested questions ===")
print(psql(f"select suggested_questions from app_model_configs where app_id='{app_id}' order by updated_at desc nulls last limit 1;"))
