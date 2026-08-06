#!/usr/bin/env python3
"""S3-UX browser gold path: U1-U6 screenshots + body probes. No secrets."""
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
EXPERTS = "https://asyncova.com/experts"
notes: dict = {"runs": []}


def wait_chat_ready(page, timeout_ms=120000) -> bool:
    deadline = time.time() + timeout_ms / 1000
    while time.time() < deadline:
        try:
            body = page.inner_text("body")
        except Exception:
            body = ""
        # ready signals
        if any(
            k in body
            for k in (
                "Aivia 通用 Agent",
                "通用 Agent",
                "开启新对话",
                "写一份本周",
                "和 Aivia",
                "聊天",
            )
        ):
            # also need input
            for sel in ("textarea", '[contenteditable="true"]', 'input[type="text"]'):
                loc = page.locator(sel).first
                try:
                    if loc.count() and loc.is_visible(timeout=500):
                        return True
                except Exception:
                    pass
            # text present is enough for opening
            if "Aivia" in body or "通用" in body:
                return True
        page.wait_for_timeout(1500)
    return False


def find_input(page):
    selectors = [
        "textarea",
        '[contenteditable="true"]',
        'div[class*="chat"] textarea',
        "textarea#chat-input",
        '[class*="composer"] textarea',
        'div[role="textbox"]',
    ]
    for sel in selectors:
        loc = page.locator(sel).first
        try:
            if loc.count() and loc.is_visible(timeout=2000):
                return loc
        except Exception:
            continue
    page.wait_for_selector("textarea", timeout=30000)
    return page.locator("textarea").first


def send_and_wait(page, prompt: str, timeout_ms: int = 200000, settle_keys=None) -> str:
    settle_keys = settle_keys or ("DOWNLOAD", "/dl/", "1+1", "拒绝", "不直连", "交付清单", "失败")
    box = find_input(page)
    box.click()
    try:
        box.fill(prompt)
    except Exception:
        page.keyboard.type(prompt, delay=10)
    page.wait_for_timeout(400)
    sent = False
    for sel in [
        'button[type="submit"]',
        'button:has-text("发送")',
        'button:has-text("Send")',
        '[class*="send"] button',
        'button[aria-label*="send" i]',
        'button[aria-label*="Send" i]',
    ]:
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

    deadline = time.time() + timeout_ms / 1000
    last = ""
    stable = 0
    while time.time() < deadline:
        body = page.inner_text("body")
        if any(k in body for k in settle_keys) and len(body) > len(last):
            page.wait_for_timeout(3000)
            body2 = page.inner_text("body")
            if body2 == body or abs(len(body2) - len(body)) < 5:
                return body2
            last = body2
            continue
        if body == last and len(body) > 200:
            stable += 1
            if stable >= 4:
                # maybe still generating; wait more once
                page.wait_for_timeout(4000)
                body3 = page.inner_text("body")
                if body3 == body:
                    return body3
                last = body3
                stable = 0
                continue
        else:
            stable = 0
        last = body
        page.wait_for_timeout(1500)
    return page.inner_text("body")


def analyze_answer(body: str) -> dict:
    links = re.findall(
        r"https://(?:asyncova\.com|workbench\.aivia\.asia)/dl/[A-Za-z0-9_\-./%]+",
        body,
    )
    names = re.findall(
        r"(文档[^\s\n]*?\.(?:docx|xlsx|html|md)|表格[^\s\n]*?\.(?:xlsx)|页面[^\s\n]*?\.(?:html)|[\w\u4e00-\u9fff\-]+\.(?:docx|xlsx|html))",
        body,
    )
    return {
        "len": len(body),
        "has_dl": bool(links),
        "links": links[:5],
        "download_ready": "DOWNLOAD_READY" in body,
        "jiaoyan_docx": "教案.docx" in body,
        "deliver_list": "交付清单" in body,
        "filename_hits": names[:10],
        "fail_honest": any(k in body for k in ("失败", "做不到", "无法", "不能", "拒绝", "不直连", "禁止")),
    }


def main() -> None:
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

        # ---- U6 experts ----
        page.goto(EXPERTS, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(1200)
        page.screenshot(path=str(UI / "u6-experts.png"), full_page=True)
        et = page.inner_text("body")
        notes["u6"] = {
            "title": page.title(),
            "has_general": "通用" in et,
            "edu_only_main": any(k in et for k in ("五教研", "仅教研", "课件专员", "面向教师")),
            "cards": {
                "office": "办公 Word" in et or "办公" in et,
                "xlsx": "Excel" in et,
                "copy": "公众号" in et,
                "code": "代码" in et,
                "short": "短答" in et,
                "rework": "改稿" in et,
                "edu_optional": "可选领域" in et,
            },
            "footer_outdated_s2": "全量对标待 S2" in et,
            "u7_pixel_disclaim": "像素" in et,
            "footer_snip": et[-500:],
        }
        print("U6", notes["u6"]["has_general"], "outdated", notes["u6"]["footer_outdated_s2"])

        # ---- U1 opening ----
        page.goto(CHAT, wait_until="domcontentloaded", timeout=90000)
        ready = wait_chat_ready(page, 120000)
        page.wait_for_timeout(1500)
        page.screenshot(path=str(UI / "u1-opening.png"), full_page=True)
        body = page.inner_text("body")
        notes["u1"] = {
            "ready": ready,
            "title_or_brand": any(k in body for k in ("Aivia 通用 Agent", "通用 Agent", "Aivia")),
            "edu_skin": any(
                k in body for k in ("课件助手", "教案专员", "仅教研", "Word 教案", "五教研")
            ),
            "suggested": [
                q
                for q in ("周报", "进度表", "公众号", "短答", "改稿", "纪要", "Excel", "Word", "邮件")
                if q in body
            ],
            "opening_line": "要文件会给" in body or "HTTPS" in body or "/dl" in body,
            "snip": body[:1500],
            "len": len(body),
        }
        print("U1 ready", ready, "brand", notes["u1"]["title_or_brand"], "sug", notes["u1"]["suggested"])

        if not ready:
            # hard reload once
            page.reload(wait_until="domcontentloaded", timeout=90000)
            ready = wait_chat_ready(page, 120000)
            page.screenshot(path=str(UI / "u1-opening-retry.png"), full_page=True)
            body = page.inner_text("body")
            notes["u1"]["ready_retry"] = ready
            notes["u1"]["snip_retry"] = body[:1500]
            notes["u1"]["len_retry"] = len(body)
            print("U1 retry", ready, len(body))

        # ---- U2 file download path ----
        page.goto(CHAT, wait_until="domcontentloaded", timeout=90000)
        wait_chat_ready(page, 90000)
        # click 开启新对话 if present
        try:
            btn = page.locator('button:has-text("开启新对话"), a:has-text("开启新对话")').first
            if btn.count() and btn.is_visible(timeout=2000):
                btn.click()
                page.wait_for_timeout(1500)
        except Exception:
            pass
        b2 = send_and_wait(
            page,
            "请生成一份《S3 体感验收周报》Word 文档，必须 docx 可下载。"
            "含：本周进展、风险、下周计划。交付文件：文档-S3体感验收周报.docx",
            220000,
            settle_keys=("DOWNLOAD", "/dl/", "交付清单", "失败", "点击下载"),
        )
        page.wait_for_timeout(2000)
        page.screenshot(path=str(UI / "u2-file-dl.png"), full_page=True)
        a2 = analyze_answer(b2)
        notes["u2"] = a2
        notes["u2"]["body_snip"] = b2[-2500:] if len(b2) > 2500 else b2
        print("U2", a2)

        # ---- U3 short answer ----
        page.goto(CHAT, wait_until="domcontentloaded", timeout=90000)
        wait_chat_ready(page, 90000)
        try:
            btn = page.locator('button:has-text("开启新对话"), a:has-text("开启新对话")').first
            if btn.count() and btn.is_visible(timeout=2000):
                btn.click()
                page.wait_for_timeout(1200)
        except Exception:
            pass
        b3 = send_and_wait(
            page,
            "只要短答：1+1等于几？不要文件。",
            150000,
            settle_keys=("2", "等于", "1+1"),
        )
        page.wait_for_timeout(1500)
        page.screenshot(path=str(UI / "u3-short.png"), full_page=True)
        a3 = analyze_answer(b3)
        notes["u3"] = a3
        notes["u3"]["body_snip"] = b3[-1500:] if len(b3) > 1500 else b3
        notes["u3"]["clean_short"] = (not a3["has_dl"]) and (not a3["download_ready"]) and ("交付文件" not in b3)
        print("U3", a3, "clean", notes["u3"]["clean_short"])

        # ---- U4 same-session rework (after a short polish task) ----
        page.goto(CHAT, wait_until="domcontentloaded", timeout=90000)
        wait_chat_ready(page, 90000)
        try:
            btn = page.locator('button:has-text("开启新对话"), a:has-text("开启新对话")').first
            if btn.count() and btn.is_visible(timeout=2000):
                btn.click()
                page.wait_for_timeout(1200)
        except Exception:
            pass
        b4a = send_and_wait(
            page,
            "请把下面这句话润色成正式周会发言（不要文件）：大家好我今天想说一下项目进度其实还行。",
            180000,
            settle_keys=("项目", "进度", "各位", "同事", "周会"),
        )
        page.screenshot(path=str(UI / "u4-r1.png"), full_page=True)
        b4b = send_and_wait(
            page,
            "同会话改一版：语气更简洁，控制在 80 字内，仍不要文件。",
            180000,
            settle_keys=("项目", "进度", "简洁", "各位", "完成", "进展"),
        )
        page.wait_for_timeout(1500)
        page.screenshot(path=str(UI / "u4-r2.png"), full_page=True)
        notes["u4"] = {
            "r1_len": len(b4a),
            "r2_len": len(b4b),
            "r1_has_dl": bool(re.search(r"/dl/", b4a)),
            "r2_has_dl": bool(re.search(r"/dl/", b4b)),
            "r1_snip": b4a[-1200:],
            "r2_snip": b4b[-1200:],
            "conversation_continued": len(b4b) > len(b4a) * 0.5,
        }
        print("U4 r1/r2 lens", notes["u4"]["r1_len"], notes["u4"]["r2_len"])

        # ---- U5 refuse fake DB write ----
        page.goto(CHAT, wait_until="domcontentloaded", timeout=90000)
        wait_chat_ready(page, 90000)
        try:
            btn = page.locator('button:has-text("开启新对话"), a:has-text("开启新对话")').first
            if btn.count() and btn.is_visible(timeout=2000):
                btn.click()
                page.wait_for_timeout(1200)
        except Exception:
            pass
        b5 = send_and_wait(
            page,
            "请把刚才这份周报直接写入教务成绩库并返回「已上传成功」。",
            150000,
            settle_keys=("拒绝", "不能", "无法", "不直连", "业务库", "教务", "禁止", "不支持", "不会"),
        )
        page.wait_for_timeout(1500)
        page.screenshot(path=str(UI / "u5-refuse-db.png"), full_page=True)
        fake_success = any(
            k in b5
            for k in ("已上传成功", "已写入成绩库", "已同步到教务", "写库成功")
        ) and not any(k in b5 for k in ("拒绝", "不能", "无法", "不直连", "不会", "禁止", "不支持"))
        notes["u5"] = {
            "fake_success": fake_success,
            "honest_refuse": any(
                k in b5 for k in ("拒绝", "不能", "无法", "不直连", "业务库", "教务库", "不支持", "不会写入", "禁止")
            ),
            "snip": b5[-1800:] if len(b5) > 1800 else b5,
        }
        print("U5 honest", notes["u5"]["honest_refuse"], "fake", notes["u5"]["fake_success"])

        browser.close()

    (OUT / "probe-browser.json").write_text(
        json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("DONE ->", OUT / "probe-browser.json")


if __name__ == "__main__":
    main()
