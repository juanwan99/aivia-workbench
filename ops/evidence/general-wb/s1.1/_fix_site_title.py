#!/usr/bin/env python3
"""Rename Dify public site title off 课件 branding. No secrets printed."""
from __future__ import annotations

import subprocess

APP = "fc3e14da-2861-4009-a888-730a6b993011"


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
            "-tAc",
            sql,
        ],
        text=True,
    ).strip()


def main() -> None:
    print("APP", psql(f"select id||'|'||name from apps where id='{APP}';"))
    print(
        "SITE_BEFORE",
        psql(
            f"select id||'|'||coalesce(title,'')||'|'||coalesce(code,'') from sites where app_id='{APP}';"
        ),
    )
    # apps.name already general; sites.title drives public chat chrome
    psql(
        f"update apps set name='Aivia 通用 Agent', updated_at=now() where id='{APP}';"
    )
    n = psql(
        f"update sites set title='Aivia 通用 Agent', updated_at=now() where app_id='{APP}' returning id;"
    )
    print("SITE_UPDATE", n)
    print(
        "SITE_AFTER",
        psql(
            f"select id||'|'||coalesce(title,'')||'|'||coalesce(code,'') from sites where app_id='{APP}';"
        ),
    )
    # flush redis so site cache refreshes
    subprocess.call(
        ["docker", "exec", "dify-redis-1", "redis-cli", "FLUSHDB"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("DONE")


if __name__ == "__main__":
    main()
