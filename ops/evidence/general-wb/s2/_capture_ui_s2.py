#!/usr/bin/env python3
"""S2 browser screenshots ≥5 — wait for completed answers. No secrets."""
from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent / "ui"
OUT.mkdir(parents=True, exist_ok=True)
CHAT = "https://asyncova.com/chat/lOMVPbz7rZmbJSJl"

G4_R1 = (
    "请生成一份《项目启动会纪要》Word 文档（必须可下载 docx）。"
    "含：会议信息、决议列表、待办（事项/负责人/日期）。"
)
G4_R2 = (
    "请在上一版基础上改一版完整文档（不要只给 diff）："
    "1) 标题改为《项目启动会纪要-v2》"
    "2) 待办表增加「优先级」列 "
    "3) 仍给我可下载的 docx。"
)
G5 = (
    "写一篇公众号推文正文：《远程办公的 5 个效率习惯》。"
    "要求：标题+导语+5 个小标题要点+结尾互动句；800 字内；"
    "只要正文，不要生成任何文件。"
)
G6 = (
    "写一个可运行的 Python3 脚本：从标准输入或同目录 data.csv 读取 CSV（首行为表头），"
    "打印每一数值列的均值；缺省文件则内置 3 行示例数据演示。"
    "请给出完整脚本（可复制代码块，或 .py 可下载二选一，须完整可运行）。"
)
G7 = (
    "请根据下列假设数据做竞品对比，输出 Excel 可下载："
    "产品A 单价99元 月销量120；产品B 单价79元 月销量200。"
    "表至少含：产品、单价、月销量、估算月营收。"
    "再给 3 条中性观察（不要投资建议、不要荐股、不要「稳赚」话术）。"
)


def send_wait(page, text: str, needles: list[str], timeout_s: int = 180) -> str:
    page.wait_for_selector("textarea", timeout=60000)
    box = page.locator("textarea").first
    box.click()
    box.fill(text)
    page.keyboard.press("Enter")
    deadline = time.time() + timeout_s
    last = ""
    stable = 0
    while time.time() < deadline:
        body = page.inner_text("body")
        # still streaming?
        streaming = "停止响应" in body or ("LLM" in body and "..." in body)
        hit = all(n in body for n in needles) if needles else False
        if hit and not streaming:
            page.wait_for_timeout(1500)
            body2 = page.inner_text("body")
            if body2 == body or abs(len(body2) - len(body)) < 8:
                return body2
        if body == last and not streaming and len(body) > 400:
            stable += 1
            if stable >= 3 and (hit or not needles):
                return body
        else:
            stable = 0
        last = body
        page.wait_for_timeout(2000)
    return page.inner_text("body")


def new_chat(page) -> None:
    try:
        page.locator("text=开启新对话").first.click(timeout=8000)
        page.wait_for_timeout(2000)
    except Exception:
        page.goto(CHAT, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(3000)


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900}, locale="zh-CN"
        )
        page = context.new_page()
        page.goto(CHAT, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(3500)
        new_chat(page)

        send_wait(page, G4_R1, ["DOWNLOAD_READY", "/dl/"], 180)
        page.screenshot(path=str(OUT / "s2-ui-g4-r1.png"), full_page=True)
        print("g4-r1", (OUT / "s2-ui-g4-r1.png").stat().st_size)

        send_wait(page, G4_R2, ["DOWNLOAD_READY", "v2"], 180)
        page.screenshot(path=str(OUT / "s2-ui-g4-r2.png"), full_page=True)
        print("g4-r2", (OUT / "s2-ui-g4-r2.png").stat().st_size)

        new_chat(page)
        body = send_wait(page, G5, ["效率习惯"], 150)
        # ensure no download in g5
        print("g5_has_dl", "/dl/" in body, "DOWNLOAD" in body)
        page.screenshot(path=str(OUT / "s2-ui-g5.png"), full_page=True)
        print("g5", (OUT / "s2-ui-g5.png").stat().st_size)

        new_chat(page)
        send_wait(page, G6, ["import", "csv"], 180)
        page.screenshot(path=str(OUT / "s2-ui-g6.png"), full_page=True)
        print("g6", (OUT / "s2-ui-g6.png").stat().st_size)

        new_chat(page)
        send_wait(page, G7, ["DOWNLOAD_READY", "/dl/"], 150)
        page.screenshot(path=str(OUT / "s2-ui-g7.png"), full_page=True)
        print("g7", (OUT / "s2-ui-g7.png").stat().st_size)

        browser.close()
        print("DONE")


if __name__ == "__main__":
    main()
