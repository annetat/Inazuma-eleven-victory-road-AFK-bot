import pyautogui
import time
import os
import sys

# -----------------------------
# Base dir (支援 PyInstaller onefile / onedir)
# -----------------------------
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# Templates folder
# -----------------------------
folder = os.path.join(BASE_DIR, "unbox")

# 防呆檢查
print("BASE_DIR =", BASE_DIR)
print("UNBOX_DIR =", folder)
if not os.path.exists(folder):
    print("❌ unbox folder missing!")
    sys.exit(1)

for f in os.listdir(folder):
    print(" -", f)

# -----------------------------
# Step settings
# -----------------------------
steps = [
    {"type": "click", "target": "1c.png", "timeout": 5,  "on_fail": 5},
    {"type": "click", "target": "2c.png", "timeout": 30, "on_fail": -1},
    {"type": "click", "target": "3c.png", "timeout": 30, "on_fail": -1},
    {"type": "click", "target": "4c.png", "timeout": 30, "delay": 1, "on_fail": -1},

    # Step 5, 6
    {"type": "wait_click", "delay": 1.5, "on_fail": 9},
    {"type": "wait_click", "delay": 1, "on_fail": 9},
]

# -----------------------------
# Main loop
# -----------------------------
while True:
    print("\n=== Starting a new loop ===")
    step_index = 0
    step_start_time = time.time()

    while step_index < len(steps):
        step = steps[step_index]
        action_type = step["type"]
        timeout = step.get("timeout", 9999)
        on_fail = step.get("on_fail", -1)

        # -----------------------------
        # Timeout handling
        # -----------------------------
        if time.time() - step_start_time > timeout:
            old_index = step_index
            if on_fail == -1:
                step_index = max(step_index - 1, 0)
                print(f"Step {old_index+1} timed out → return to step {step_index+1}")
            else:
                if on_fail >= len(steps):
                    print(f"Step {old_index+1} timed out → on_fail step {on_fail+1} out of range → restart loop")
                    break
                step_index = on_fail
                print(f"Step {old_index+1} timed out → jump to step {on_fail+1}")
            step_start_time = time.time()
            continue

        try:
            # -----------------------------
            # Click image (支援 delay)
            # -----------------------------
            if action_type == "click":
                img_path = os.path.join(folder, step["target"])
                location = pyautogui.locateOnScreen(img_path, confidence=0.85)

                if location:
                    delay = step.get("delay", 0)
                    if delay > 0:
                        print(f"Step {step_index+1}: wait {delay}s before click")
                        time.sleep(delay)

                    x, y = pyautogui.center(location)
                    pyautogui.moveTo(x, y, duration=0)
                    pyautogui.click()
                    print(f"Step {step_index+1}: Clicked {step['target']}")
                    step_index += 1
                    step_start_time = time.time()

            # -----------------------------
            # Wait then click
            # -----------------------------
            elif action_type == "wait_click":
                delay = step.get("delay", 0)
                print(f"Step {step_index+1}: wait {delay}s then click")
                time.sleep(delay)
                pyautogui.click()
                step_index += 1
                step_start_time = time.time()

        except pyautogui.ImageNotFoundException:
            pass

        time.sleep(0.2)

    print("=== One loop completed, restarting ===")
    time.sleep(2)
