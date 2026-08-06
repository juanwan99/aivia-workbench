"""Live WorkBuddy UI capture — no reverse engineering."""
import time
import os
from pathlib import Path

import win32gui
import win32con
import win32api
from PIL import ImageGrab

OUT = Path(__file__).resolve().parent / "ui"
OUT.mkdir(parents=True, exist_ok=True)


def find_wb():
    found = []

    def enum(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title == "WorkBuddy" or title.startswith("WorkBuddy"):
                found.append(hwnd)
        return True

    win32gui.EnumWindows(enum, None)
    return found[0] if found else None


def main():
    hwnd = find_wb()
    if not hwnd:
        os.startfile(r"C:\Users\liang\AppData\Local\Programs\WorkBuddy\WorkBuddy.exe")
        for _ in range(25):
            time.sleep(1)
            hwnd = find_wb()
            if hwnd:
                break
    print("HWND", hwnd, "title", win32gui.GetWindowText(hwnd) if hwnd else None)
    if not hwnd:
        raise SystemExit("no WorkBuddy window")

    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    try:
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        print("foreground warn", e)
    time.sleep(0.8)
    l, t, r, b = win32gui.GetWindowRect(hwnd)
    print("rect", l, t, r, b, "size", r - l, b - t)

    def cap(name: str):
        time.sleep(1.0)
        ll, tt, rr, bb = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox=(ll, tt, rr, bb))
        p = OUT / name
        img.save(p)
        print("CAP", name, p.stat().st_size)

    def click_rel(rx: int, ry: int):
        ll, tt, rr, bb = win32gui.GetWindowRect(hwnd)
        x, y = ll + rx, tt + ry
        print(f"click {x},{y} rel {rx},{ry}")
        try:
            win32gui.SetForegroundWindow(hwnd)
        except Exception:
            pass
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(0.95)

    cap("live-01-main.png")

    # Sidebar (approx for 1452x877)
    click_rel(100, 95)
    cap("live-02-newtask.png")
    click_rel(100, 130)
    cap("live-03-assistant.png")
    click_rel(100, 165)
    cap("live-04-project.png")

    # Project tabs
    click_rel(490, 115)
    cap("live-04b-project-tasks.png")
    click_rel(560, 115)
    cap("live-04c-project-assets.png")
    click_rel(420, 115)
    cap("live-04d-project-plan.png")
    click_rel(350, 115)
    cap("live-04e-project-activity.png")

    # Experts / automation / more
    click_rel(100, 200)
    cap("live-05-experts.png")
    click_rel(100, 235)
    cap("live-06-automation.png")
    click_rel(100, 270)
    cap("live-07-more.png")

    # History tasks in left rail
    click_rel(120, 340)
    cap("live-08-history-task1.png")
    click_rel(120, 375)
    cap("live-08b-history-task2.png")

    # New task + composer +
    click_rel(100, 95)
    time.sleep(0.5)
    click_rel(320, 500)
    cap("live-09-composer-plus.png")
    click_rel(360, 555)
    cap("live-10-workspace-perm.png")

    # Account / search
    click_rel(55, 835)
    cap("live-11-account.png")
    click_rel(70, 55)
    cap("live-12-search.png")

    print("DONE")
    for p in sorted(OUT.glob("live-*.png")):
        print(p.name, p.stat().st_size)


if __name__ == "__main__":
    main()
