import pyautogui
import time
import os
import sys

# -----------------------------
# Folder path (relative, pure Python version)
# -----------------------------
folder = os.path.join(os.path.dirname(__file__), "free")

if not os.path.exists(folder):
    print(f"free folder not found. Please make sure {folder} exists.")
    sys.exit(1)

# -----------------------------
# Step settings
# -----------------------------
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
    {"type": "key",   "target": "u",          "timeout": 30,  "on_fail": -1},
    {"type": "click", "target": "Picture6.png", "timeout": 300, "on_fail": 8},
    {"type": "click", "target": "Picture7.png", "timeout": 300, "on_fail": -1, "wait_after_move": 3},
    {"type": "click", "target": "Picture9.png", "timeout": 30, "on_fail": -1, "wait_after_move": 3} 
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
        target = step["target"]
        timeout = step["timeout"]
        on_fail = step["on_fail"]
        wait_after_move = step.get("wait_after_move", 1)

        # Timeout handling
        if time.time() - step_start_time > timeout:
            old_index = step_index
            if on_fail == -1:
                step_index = max(step_index - 1, 0)
                print(f"Step {old_index+1} timed out after {timeout} seconds → return to step {step_index+1}")
            else:
                step_index = on_fail
                print(f"Step {old_index+1} timed out after {timeout} seconds → jump to step {on_fail+1}")
            step_start_time = time.time()
            continue

        # Execute step
        try:
            if action_type == "click":
                img_path = os.path.join(folder, target)
                location = pyautogui.locateOnScreen(img_path, confidence=0.90)

                if location:
                    center_x, center_y = pyautogui.center(location)
                    pyautogui.moveTo(center_x, center_y, duration=1.0)
                    print(f"Mouse moved to ({center_x},{center_y}), waiting {wait_after_move} seconds...")
                    time.sleep(wait_after_move)
                    pyautogui.click()
                    print(f"Completed step {step_index+1}: Clicked {target}")
                    step_index += 1
                    step_start_time = time.time()

            elif action_type == "key":
                pyautogui.press(target)
                print(f"Step {step_index+1}: Pressed {target.upper()}")
                step_index += 1
                step_start_time = time.time()

        except pyautogui.ImageNotFoundException:
            pass

        time.sleep(1)

    print("=== One loop completed, restarting ===")
    time.sleep(2)