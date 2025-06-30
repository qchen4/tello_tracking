"""
Tello Drone Object Tracker (Configurable HSV + Presets)

This script uses computer vision to track a colored object using a DJI Tello drone.
You can either select from built-in color presets or load custom HSV thresholds from a JSON config.

Features:
- Real-time object tracking based on HSV masking
- User prompt to choose default or tuned HSV config
- Modular detection logic
- Command-line control: takeoff, start tracking, land, exit
- Safe landing and resource cleanup on quit

Author: Qiyue Chen
Date: 2025-06-30
"""

import cv2
import numpy as np
import time
import json
from djitellopy import Tello

# ---------------------------------------------
# HSV Color Presets
# ---------------------------------------------

COLOR_PRESETS = {
    "green": {
        "lower": [40, 70, 70],
        "upper": [80, 255, 255]
    },
    "red": {
        "lower": [0, 120, 70],
        "upper": [10, 255, 255]
    },
    "blue": {
        "lower": [100, 150, 0],
        "upper": [140, 255, 255]
    }
}

# ---------------------------------------------
# Load HSV Configuration
# ---------------------------------------------

def load_hsv_config():
    """
    Prompt user to select a color or load a custom config from hsv_config.json.

    Returns:
        tuple: lower and upper HSV bounds as NumPy arrays
    """
    print("Select tracking color:")
    print("1 - Green (default)")
    print("2 - Red")
    print("3 - Blue")
    print("4 - Load from hsv_config.json")

    choice = input("Enter choice [1-4]: ").strip()

    if choice == '1':
        hsv = COLOR_PRESETS["green"]
    elif choice == '2':
        hsv = COLOR_PRESETS["red"]
    elif choice == '3':
        hsv = COLOR_PRESETS["blue"]
    elif choice == '4':
        try:
            with open("hsv_config.json", "r") as f:
                hsv = json.load(f)
        except Exception as e:
            print("Failed to load hsv_config.json:", e)
            print("Falling back to green.")
            hsv = COLOR_PRESETS["green"]
    else:
        print("Invalid input. Using default green.")
        hsv = COLOR_PRESETS["green"]

    lower = np.array(hsv["lower"])
    upper = np.array(hsv["upper"])
    return lower, upper

# ---------------------------------------------
# Object Detection
# ---------------------------------------------

def detect_object(frame, lower, upper):
    """
    Detect the largest object matching the HSV mask in the frame.

    Parameters:
        frame (np.ndarray): Input BGR frame from the drone
        lower (np.ndarray): Lower HSV threshold
        upper (np.ndarray): Upper HSV threshold

    Returns:
        tuple: (x, y) of object center if found, and the binary mask
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > 300:
            x, y, w, h = cv2.boundingRect(c)
            return (x + w // 2, y + h // 2), mask
    return None, mask

# ---------------------------------------------
# Main Function
# ---------------------------------------------

def main():
    # Load HSV thresholds
    lower_hsv, upper_hsv = load_hsv_config()

    # Initialize Tello
    tello = Tello()
    tello.connect()
    tello.streamon()

    # Frame settings
    frame_width, frame_height = 640, 480
    center_x, center_y = frame_width // 2, frame_height // 2
    tolerance = 40  # pixel offset tolerance

    print("\n--- Tello Tracker Commands ---")
    print("Type one of the following commands:")
    print("[takeoff]    - Launch drone")
    print("[start]      - Start object tracking")
    print("[land]       - Land the drone")
    print("[exit]       - Exit program\n")

    flying = False
    tracking = False

    try:
        while True:
            # Read user input
            cmd = input("Command > ").strip().lower()

            if cmd == "takeoff":
                if not flying:
                    tello.takeoff()
                    flying = True
                    print("Drone has taken off.")
                else:
                    print("Drone is already flying.")

            elif cmd == "start":
                if not flying:
                    print("Please take off before starting tracking.")
                    continue
                print("Starting object tracking...")
                tracking = True

                # Tracking loop
                while tracking:
                    frame = tello.get_frame_read().frame
                    frame = cv2.resize(frame, (frame_width, frame_height))

                    center, mask = detect_object(frame, lower_hsv, upper_hsv)

                    if center:
                        cv2.circle(frame, center, 10, (0, 255, 0), -1)

                        offset_x = center[0] - center_x
                        offset_y = center_y - center[1]

                        if offset_x < -tolerance:
                            tello.move_left(20)
                        elif offset_x > tolerance:
                            tello.move_right(20)

                        if offset_y > tolerance:
                            tello.move_up(20)
                        elif offset_y < -tolerance:
                            tello.move_down(20)

                    cv2.imshow("Tello View", frame)
                    cv2.imshow("Mask", mask)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        print("Exiting tracking mode.")
                        tracking = False
                        break

                # Close OpenCV windows when tracking ends
                if cv2.getWindowProperty("Tello View", cv2.WND_PROP_VISIBLE) >= 1:
                    cv2.destroyAllWindows()

            elif cmd == "land":
                if flying:
                    tello.land()
                    flying = False
                    print("Drone landed.")
                else:
                    print("Drone is not flying.")

            elif cmd == "exit":
                break

            else:
                print("Unknown command. Try: takeoff, start, land, exit")

    finally:
        if flying:
            tello.land()
        tello.streamoff()
        if cv2.getWindowProperty("Tello View", cv2.WND_PROP_VISIBLE) >= 1:
            cv2.destroyAllWindows()
        print("Shut down complete.")

# ---------------------------------------------
# Entry Point
# ---------------------------------------------

if __name__ == "__main__":
    main()
