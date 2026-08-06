#!/usr/bin/env python3
"""S1.1 browser screenshots (no secrets)."""
from __future__ import annotations

import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "ui"
OUT.mkdir(parents=True, exist_ok=True)
CHAT = "https://asyncova.com/chat/lOMVPbz7rZmbJSJl"
EXPERTS = "https://asyncova.com/experts"


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            locale="zh-CN",
        )
        page = context.new_page()

        # ui-experts
        page.goto(EXPERTS, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(800)
        page.screenshot(path=str(OUT / "ui-experts.png"), full_page=True)
        print("shot", OUT / "ui-experts.png")

        # ui-chat-opening
        page.goto(CHAT, wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(2500)
        page.screenshot(path=str(OUT / "ui-chat-opening.png"), full_page=True)
        print("shot", OUT / "ui-chat-opening.png")

        def send_and_wait(prompt: str, timeout_ms: int = 180000) -> None:
            # Dify web chat: textarea / contenteditable
            selectors = [
                "textarea",
                '[contenteditable="true"]',
                'div[class*="chat"] textarea',
                "textarea#chat-input",
            ]
            box = None
            for sel in selectors:
                loc = page.locator(sel).first
                try:
                    if loc.count() and loc.is_visible(timeout=2000):
                        box = loc
                        break
                except Exception:
                    continue
            if box is None:
                # last resort: any textarea
                page.wait_for_selector("textarea", timeout=30000)
                box = page.locator("textarea").first
            box.click()
            box.fill(prompt)
            page.wait_for_timeout(300)
            # send button variants
            sent = False
            for sel in [
                'button[type="submit"]',
                'button:has-text("发送")',
                'button:has-text("Send")',
                '[class*="send"] button',
                'button[aria-label*="send" i]',
            ]:
                try:
                    b = page.locator(sel).first
                    if b.count() and b.is_visible(timeout=1000):
                        b.click()
                        sent = True
                        break
                except Exception:
                    continue
            if not sent:
                page.keyboard.press("Enter")
            # wait for answer growth / download markers
            deadline = time.time() + timeout_ms / 1000
            last = ""
            while time.time() < deadline:
                body = page.inner_text("body")
                if body != last and len(body) > len(last) + 20:
                    # settle a bit
                    page.wait_for_timeout(2500)
                    body2 = page.inner_text("body")
                    if body2 == body or "DOWNLOAD" in body2 or "/dl/" in body2 or "2" in body2:
                        return
                last = body
                page.wait_for_timeout(1500)
            print("WARN: wait timed out for", prompt[:40])

        # ui-g1-dl
        page.goto(CHAT, wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(1500)
        send_and_wait(
            "请生成一份《Q3 项目周报》Word 文档，必须 docx 可下载。含：本周进展、风险、下周计划。",
            180000,
        )
        page.wait_for_timeout(2000)
        page.screenshot(path=str(OUT / "ui-g1-dl.png"), full_page=True)
        print("shot", OUT / "ui-g1-dl.png")
        body = page.inner_text("body")
        print("g1 has_dl", bool(re.search(r"/dl/", body)), "download", "DOWNLOAD" in body)

        # ui-g3-short (new conversation: reload)
        page.goto(CHAT, wait_until="networkidle", timeout=90000)
        page.wait_for_timeout(1500)
        send_and_wait("只要短答：1+1等于几？不要文件。", 120000)
        page.wait_for_timeout(1500)
        page.screenshot(path=str(OUT / "ui-g3-short.png"), full_page=True)
        print("shot", OUT / "ui-g3-short.png")
        body = page.inner_text("body")
        print("g3 has_dl", bool(re.search(r"/dl/", body)), "len_body", len(body))

        browser.close()
        print("DONE shots in", OUT)


if __name__ == "__main__":
    main()
