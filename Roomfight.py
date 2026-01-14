import pyautogui
import time
import os
import sys

# -----------------------------
# Folder path
# -----------------------------
folder = os.path.join(os.path.dirname(__file__), "room")

if not os.path.exists(folder):
    print(f"Templates folder not found. Please make sure {folder} exists.")
    sys.exit(1)

# -----------------------------
# Step settings
# -----------------------------
steps = [
    {"type": "click",    "target": "rk1.png", "timeout": 10, "on_fail": 13, "delay": 2},
    {"type": "wait_click","on_fail": 9, "delay": 2, },
    {"type": "click",    "target": "rk2.png", "delay": 2},
    {"type": "click",    "target": "rk3.png", "delay": 2},
    {"type": "click",    "target": "rk4.png", "on_fail": 9, "delay": 2},
    {"type": "wait_click","on_fail": 9, "delay": 2, },
    {"type": "click",    "target": "rk4.png", "on_fail": 9, "delay": 2},
    {"type": "click",    "target": "rk4.png", "on_fail": 9, "delay": 2},
    {"type": "wait_click", "on_fail": 9, "delay": 2,},
    {"type": "click",    "target": "rk4.png", "on_fail": 9, "delay": 2},
    {"type": "wait_key", "target": "rk5.png", "key": "u", "delay": 2},
    {"type": "click",    "target": "rk6.png", "delay": 2},
    {"type": "click",    "target": "rk7.png", "delay": 2},
    {"type": "click",    "target": "rk8.png", "timeout": 30, "on_fail": 0, "delay": 2},
]

# -----------------------------
# Main loop
# -----------------------------
while True:
    print("\n=== Starting a new loop ===")

    step_index = 0
    step_start_time = time.time()
    last_action_time = time.time()

    while step_index < len(steps):

        # =====================================================
        # 🔒 Global idle protection (600 seconds)
        # =====================================================
        if time.time() - last_action_time > 600:
            screen_w, screen_h = pyautogui.size()
            pyautogui.moveTo(screen_w // 2, screen_h // 2, duration=1)
            pyautogui.click()
            print("⚠️ No action for 600s → click center & restart")
            step_index = 0
            step_start_time = time.time()
            last_action_time = time.time()
            continue
        # =====================================================

        step = steps[step_index]
        action_type = step.get("type")
        target = step.get("target")
        timeout = step.get("timeout", 30)
        on_fail = step.get("on_fail", None)  # 默認 None，不回到上一個步驟
        delay = step.get("delay", 0)
        key = step.get("key")

        # -----------------------------
        # Step timeout handling
        # -----------------------------
        if time.time() - step_start_time > timeout:
            old_index = step_index
            if on_fail is not None:
                step_index = on_fail
                print(f"Step {old_index+1} timed out → jump to step {on_fail+1}")
            else:
                # 超時但沒有指定跳轉，保持在當前步驟重試
                print(f"Step {old_index+1} timed out → retrying current step")
            step_start_time = time.time()
            continue

        try:
            # -----------------------------
            # Click step (滑到目標後等待再點擊)
            # -----------------------------
            if action_type == "click" and target:
                img_path = os.path.join(folder, target)
                location = pyautogui.locateOnScreen(img_path, confidence=0.85)
                if location:
                    x, y = pyautogui.center(location)
                    pyautogui.moveTo(x, y, duration=1)
                    
                    if delay > 0:
                        print(f"Step {step_index+1}: Waiting {delay}s on target before clicking")
                        time.sleep(delay)

                    pyautogui.click()
                    print(f"Completed step {step_index+1}: Clicked {target}")
                    
                    step_index += 1
                    step_start_time = time.time()
                    last_action_time = time.time()

            # -----------------------------
            # Wait & press key step
            # -----------------------------
            elif action_type == "wait_key" and target:
                img_path = os.path.join(folder, target)
                location = pyautogui.locateOnScreen(img_path, confidence=0.85)
                if location:
                    print(f"Detected {target}, waiting {delay}s then pressing {key.upper()}")
                    time.sleep(delay)
                    pyautogui.press(key)
                    print(f"Completed step {step_index+1}: Pressed {key.upper()}")
                    
                    step_index += 1
                    step_start_time = time.time()
                    last_action_time = time.time()

            # -----------------------------
            # Wait click step (純等待後點擊)
            # -----------------------------
            elif action_type == "wait_click":
                print(f"Step {step_index+1}: Waiting {delay}s then clicking")
                time.sleep(delay)
                pyautogui.click()
                step_index += 1
                step_start_time = time.time()
                last_action_time = time.time()

        except pyautogui.ImageNotFoundException:
            pass

        time.sleep(1)

    print("=== One loop completed, restarting ===")
    time.sleep(2)
