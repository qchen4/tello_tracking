"""
HSV Calibrator Tool for Color Tracking (OpenCV-based)

This tool opens a webcam stream and provides interactive HSV sliders
to help the user tune HSV color thresholds. It displays:

- The original frame
- The HSV mask
- The filtered (masked) image

Press 's' to save the current HSV range to `hsv_config.json`.
Press 'q' to quit.

Author: Qiyue Chen
Date: 2025-06-30
"""

import cv2
import numpy as np
import json

def nothing(x):
    """Dummy callback for trackbar (required by OpenCV)."""
    pass

# Initialize webcam
cap = cv2.VideoCapture(0)

# Create a trackbar window and sliders for HSV range
cv2.namedWindow("Trackbars", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Trackbars", 400, 300)

cv2.createTrackbar("H Low", "Trackbars", 40, 179, nothing)
cv2.createTrackbar("S Low", "Trackbars", 70, 255, nothing)
cv2.createTrackbar("V Low", "Trackbars", 70, 255, nothing)
cv2.createTrackbar("H High", "Trackbars", 80, 179, nothing)
cv2.createTrackbar("S High", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("V High", "Trackbars", 255, 255, nothing)

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Read HSV thresholds from sliders
    hL = cv2.getTrackbarPos("H Low", "Trackbars")
    sL = cv2.getTrackbarPos("S Low", "Trackbars")
    vL = cv2.getTrackbarPos("V Low", "Trackbars")
    hH = cv2.getTrackbarPos("H High", "Trackbars")
    sH = cv2.getTrackbarPos("S High", "Trackbars")
    vH = cv2.getTrackbarPos("V High", "Trackbars")

    lower = np.array([hL, sL, vL])
    upper = np.array([hH, sH, vH])

    # Create mask and filtered result
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Resize for better layout (optional)
    frame_small = cv2.resize(frame, (400, 300))
    mask_small = cv2.resize(mask, (400, 300))
    result_small = cv2.resize(result, (400, 300))

    # Show in organized windows
    cv2.imshow("1. Original Frame", frame_small)
    cv2.imshow("2. HSV Mask", mask_small)
    cv2.imshow("3. Filtered Result", result_small)

    # Position windows
    cv2.moveWindow("Trackbars", 10, 10)
    cv2.moveWindow("1. Original Frame", 450, 10)
    cv2.moveWindow("2. HSV Mask", 450, 320)
    cv2.moveWindow("3. Filtered Result", 450, 630)

    # Key controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        with open("hsv_config.json", "w") as f:
            json.dump({"lower": lower.tolist(), "upper": upper.tolist()}, f)
        print("✅ HSV range saved to hsv_config.json.")
    elif key == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
