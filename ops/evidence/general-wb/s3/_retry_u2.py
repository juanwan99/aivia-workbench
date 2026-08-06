#!/usr/bin/env python3
"""S3 U2 retry: wait until stop-button gone + /dl present. Also re-shot U6 after footer fix if needed."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
UI = OUT / "ui"
CHAT = "https://asyncova.com/chat/lOMVPbz7rZmbJSJl"
EXPERTS = "https://asyncova.com/experts"


def wait_ready(page, timeout_ms=90000):
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        body = page.inner_text("body")
        if "Aivia 通用 Agent" in body or "开启新对话" in body:
            return True
        page.wait_for_timeout(1000)
    return False


def find_input(page):
    for sel in ("textarea", '[contenteditable="true"]', 'div[role="textbox"]'):
        loc = page.locator(sel).first
        try:
            if loc.count() and loc.is_visible(timeout=1500):
                return loc
        except Exception:
            pass
    page.wait_for_selector("textarea", timeout=30000)
    return page.locator("textarea").first


def still_generating(page) -> bool:
    body = page.inner_text("body")
    if "停止响应" in body:
        return True
    # spinning LLM row without Answer
    if re.search(r"\bLLM\b", body) and "Answer" not in body and "/dl/" not in body:
        return True
    return False


def send(page, prompt: str):
    box = find_input(page)
    box.click()
    box.fill(prompt)
    page.wait_for_timeout(300)
    sent = False
    for sel in (
        'button[type="submit"]',
        'button:has-text("发送")',
        'button[aria-label*="send" i]',
    ):
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
        if still_generating(page):
            stable = 0
            page.wait_for_timeout(2000)
            continue
        body = page.inner_text("body")
        if "/dl/" in body or "DOWNLOAD_READY" in body or "交付清单" in body:
            page.wait_for_timeout(2500)
            return page.inner_text("body")
        if "失败" in body and "下载" in body:
            page.wait_for_timeout(1500)
            return page.inner_text("body")
        if body == last:
            stable += 1
            if stable >= 6 and len(body) > 500:
                return body
        else:
            stable = 0
        last = body
        page.wait_for_timeout(2000)
    return page.inner_text("body")


def main():
    notes = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            locale="zh-CN",
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        page = context.new_page()

        # experts after potential deploy
        page.goto(EXPERTS, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(1000)
        page.screenshot(path=str(UI / "u6-experts.png"), full_page=True)
        et = page.inner_text("body")
        notes["u6"] = {
            "footer_outdated_s2": "全量对标待 S2" in et,
            "claim_general": "CLAIM-GENERAL-WB" in et or "行为对标" in et,
            "pixel": "像素" in et,
            "beian": "备案" in et,
            "footer": et[-450:],
        }
        print("U6 outdated", notes["u6"]["footer_outdated_s2"])

        # U2
        page.goto(CHAT, wait_until="domcontentloaded", timeout=90000)
        wait_ready(page)
        try:
            btn = page.locator('button:has-text("开启新对话")').first
            if btn.count() and btn.is_visible(timeout=2000):
                btn.click()
                page.wait_for_timeout(1500)
        except Exception:
            pass
        prompt = (
            "请生成一份《S3 体感验收周报》Word 文档，必须 docx 可下载。"
            "含：本周进展、风险、下周计划。交付文件：文档-S3体感验收周报.docx"
        )
        send(page, prompt)
        # wait a beat then poll
        page.wait_for_timeout(3000)
        body = wait_done(page, 300000)
        page.wait_for_timeout(2000)
        page.screenshot(path=str(UI / "u2-file-dl.png"), full_page=True)
        links = re.findall(
            r"https://(?:asyncova\.com|workbench\.aivia\.asia)/dl/[A-Za-z0-9_\-./%]+",
            body,
        )
        notes["u2"] = {
            "has_dl": bool(links),
            "links": links[:5],
            "download_ready": "DOWNLOAD_READY" in body,
            "deliver_list": "交付清单" in body,
            "jiaoyan_docx": "教案.docx" in body,
            "display_name_topic": any(
                k in body
                for k in (
                    "文档-S3体感验收周报",
                    "S3体感验收周报",
                    "体感验收周报",
                    "周报.docx",
                    "文档-",
                )
            )
            and "教案.docx" not in body,
            "snip": body[-3000:] if len(body) > 3000 else body,
            "generating_stuck": "停止响应" in body and not links,
        }
        print("U2", {k: notes["u2"][k] for k in notes["u2"] if k != "snip"})

        # public HEAD on first link
        if links:
            import urllib.request

            url = links[0]
            try:
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=30) as resp:
                    blob = resp.read()
                    cd = resp.headers.get("Content-Disposition") or ""
                    notes["u2"]["public_status"] = resp.status
                    notes["u2"]["public_size"] = len(blob)
                    notes["u2"]["content_disposition"] = cd
                    notes["u2"]["ooxml_zip"] = blob[:2] == b"PK"
                    # save local
                    dest = OUT / "u2-week-report.docx"
                    dest.write_bytes(blob)
                    notes["u2"]["saved"] = str(dest)
                    print("downloaded", len(blob), cd[:120])
            except Exception as e:
                notes["u2"]["public_err"] = str(e)[:200]
                print("dl err", e)

        # light U4 docx rework if U2 ok - same session
        if notes["u2"].get("has_dl"):
            send(
                page,
                "同会话改稿：在上一版基础上增加「本周结论」一节，交付文件：文档-S3体感验收周报-v2.docx",
            )
            page.wait_for_timeout(3000)
            body2 = wait_done(page, 300000)
            page.wait_for_timeout(1500)
            page.screenshot(path=str(UI / "u4-r2-file.png"), full_page=True)
            links2 = re.findall(
                r"https://(?:asyncova\.com|workbench\.aivia\.asia)/dl/[A-Za-z0-9_\-./%]+",
                body2,
            )
            notes["u4_file"] = {
                "has_dl": bool(links2),
                "links": links2[:5],
                "v2_name": "v2" in body2 or "改" in body2,
                "snip": body2[-2000:],
            }
            print("U4file", notes["u4_file"]["has_dl"], notes["u4_file"]["v2_name"])

        browser.close()

    (OUT / "probe-u2-retry.json").write_text(
        json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("DONE")


if __name__ == "__main__":
    main()
