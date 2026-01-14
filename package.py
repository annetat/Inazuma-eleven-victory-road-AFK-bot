import pyautogui
import time
import os
import sys
import traceback
from pyscreeze import ImageNotFoundException

# =========================================================
# Base dir (支援 PyInstaller onefile / onedir)
# =========================================================


# 指向 exe 旁的資料夾，而不是臨時解壓路徑
BASE_DIR = os.path.dirname(sys.executable)  # exe 的路徑
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

print(f"TEMPLATE DIR: {TEMPLATE_DIR}")

if not os.path.isdir(TEMPLATE_DIR):
    print(f"Templates folder not found: {TEMPLATE_DIR}")
    sys.exit(1)


# =========================================================
# Steps config
# =========================================================
steps = [
    {"type": "click", "target": "Picture1.png", "timeout": 10,  "on_fail": 12},
    {"type": "click", "target": "Picture2.png", "timeout": 30,  "on_fail": -1},
    {"type": "click", "target": "Picture3.png", "timeout": 30,  "on_fail": -1},
    {"type": "click", "target": "Picture4.png", "timeout": 30,  "on_fail": -1},
    {"type": "click", "target": "Picture5.png", "timeout": 30,  "on_fail": -1},
    {"type": "click", "target": "Picture6.png", "timeout": 30,  "on_fail": -1},
    {"type": "click", "target": "Picture7.png", "timeout": 30,  "on_fail": -1},
    {"type": "click", "target": "Picture7.png", "timeout": 30,  "on_fail": -1},
    {"type": "click", "target": "Picture8.png", "timeout": 10,  "on_fail": -1},
    {"type": "key",   "target": "u",            "timeout": 30,  "on_fail": -1},
    {"type": "click", "target": "Picture6.png", "timeout": 300, "on_fail": 8},
    {"type": "click", "target": "Picture7.png", "timeout": 300, "on_fail": -1, "wait_after_move": 3},
    {"type": "click", "target": "Picture9.png", "timeout": 30,  "on_fail": -1, "wait_after_move": 3},
]

# =========================================================
# Main loop
# =========================================================
while True:
    print("\n=== Starting a new loop ===")
    step_index = 0
    step_start_time = time.time()

    while step_index < len(steps):
        step = steps[step_index]T
        action_type = step["type"]
        target = step["target"]
        timeout = step["timeout"]
        on_fail = step["on_fail"]
        wait_after_move = step.get("wait_after_move", 1)

        # ---------------- Timeout handling ----------------
        if time.time() - step_start_time > timeout:
            old = step_index
            if on_fail == -1:
                step_index = max(step_index - 1, 0)
                print(f"⏱ Step {old+1} timeout → back to step {step_index+1}")
            else:
                step_index = on_fail
                print(f"⏱ Step {old+1} timeout → jump to step {on_fail+1}")
            step_start_time = time.time()
            continue

        try:
            # ---------------- CLICK ----------------
            if action_type == "click":
                img_path = os.path.join(TEMPLATE_DIR, target)

                if not os.path.isfile(img_path):
                    print(f"⚠ Image missing: {target}")
                    time.sleep(1)
                    continue

                location = pyautogui.locateOnScreen(
                    img_path,
                    confidence=0.65,
                    grayscale=True
                )

                if location:
                    x, y = pyautogui.center(location)
                    pyautogui.moveTo(x, y, duration=0.8)
                    time.sleep(wait_after_move)
                    pyautogui.click()
                    print(f"✔ Step {step_index+1}: Click {target}")
                    step_index += 1
                    step_start_time = time.time()

            # ---------------- KEY ----------------
            elif action_type == "key":
                pyautogui.press(target)
                print(f"✔ Step {step_index+1}: Press {target.upper()}")
                step_index += 1
                step_start_time = time.time()

        # ✅ 找不到圖片＝正常 → 完全忽略
        except (pyautogui.ImageNotFoundException, ImageNotFoundException):
            time.sleep(1)

        # ❌ 真的程式錯誤才顯示
        except Exception as e:
            print(f"❌ Fatal error at step {step_index+1}")
            print(repr(e))
            traceback.print_exc()
            time.sleep(2)

        time.sleep(1)

    print("=== Loop finished, restarting ===")
    time.sleep(2)
