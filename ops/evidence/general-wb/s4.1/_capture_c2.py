#!/usr/bin/env python3
"""Browser shot for S4.1 F5: same-session C2 rework."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
UI = OUT / "ui"
UI.mkdir(parents=True, exist_ok=True)
CHAT = "https://asyncova.com/chat/lOMVPbz7rZmbJSJl"


def wait_ready(page) -> bool:
    for _ in range(60):
        b = page.inner_text("body")
        if "Aivia 通用 Agent" in b or "开启新对话" in b:
            return True
        page.wait_for_timeout(1000)
    return False


def find_input(page):
    for sel in ("textarea", '[contenteditable="true"]'):
        loc = page.locator(sel).first
        try:
            if loc.count() and loc.is_visible(timeout=1500):
                return loc
        except Exception:
            pass
    page.wait_for_selector("textarea", timeout=30000)
    return page.locator("textarea").first


def send(page, prompt: str) -> None:
    box = find_input(page)
    box.click()
    box.fill(prompt)
    page.wait_for_timeout(300)
    sent = False
    for sel in ('button[type="submit"]', 'button:has-text("发送")'):
        try:
            b = page.locator(sel).first
            if b.count() and b.is_visible(timeout=800):
                b.click()
                sent = True
                break
        except Exception:
            continue
    if not sent:
        page.keyboard.press("Enter")


def wait_done(page, timeout_ms=300000) -> str:
    deadline = time.time() + timeout_ms / 1000
    last = ""
    stable = 0
    while time.time() < deadline:
        body = page.inner_text("body")
        if "停止响应" in body:
            page.wait_for_timeout(2000)
            continue
        if "/dl/" in body or "DOWNLOAD_READY" in body or "交付清单" in body:
            page.wait_for_timeout(2500)
            return page.inner_text("body")
        if body == last:
            stable += 1
            if stable >= 6:
                return body
        else:
            stable = 0
        last = body
        page.wait_for_timeout(2000)
    return page.inner_text("body")


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context(
            viewport={"width": 1440, "height": 900}, locale="zh-CN"
        ).new_page()
        page.goto(CHAT, wait_until="domcontentloaded", timeout=90000)
        wait_ready(page)
        try:
            btn = page.locator('button:has-text("开启新对话")').first
            if btn.count() and btn.is_visible(timeout=2000):
                btn.click()
                page.wait_for_timeout(1200)
        except Exception:
            pass

        send(
            page,
            "做一张竞品表 Excel：产品A 单价99 月销120；产品B 单价79 月销200。"
            "列含产品、单价、月销量、估算月营收。交付文件：表格-竞品-v1.xlsx",
        )
        b1 = wait_done(page)
        page.screenshot(path=str(UI / "s4-c2-r1.png"), full_page=True)
        print("r1 dl", bool(re.search(r"/dl/", b1)))

        send(
            page,
            "同会话完整再加工：输出完整新文件。"
            "增加市占率列 A=40 B=60；新增产品C 单价89 月销150 市占20；"
            "营收=单价×月销量；必须 csv 业务数据；交付文件：表格-竞品-v2.xlsx",
        )
        b2 = wait_done(page)
        page.wait_for_timeout(1500)
        page.screenshot(path=str(UI / "s4-c2-rework.png"), full_page=True)
        notes = {
            "r2_has_dl": bool(re.search(r"/dl/", b2)),
            "r2_ids": list(dict.fromkeys(re.findall(r"/dl/([a-f0-9]+)/", b2))),
            "jiaoyan": "教案.docx" in b2,
            "has_v2_name": "v2" in b2 or "竞品" in b2,
            "nested_ui": "文件名" in b2 and "点击下载" in b2 and "市占" not in b2,
        }
        print(notes)
        (OUT / "probe-c2-browser.json").write_text(
            json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        browser.close()
        print("DONE", UI / "s4-c2-rework.png")


if __name__ == "__main__":
    main()
