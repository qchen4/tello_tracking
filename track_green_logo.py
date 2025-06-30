"""
Tello Drone Green Object Tracker (OpenCV + HSV)

This script controls a DJI Tello drone using computer vision to detect and track a green-colored object 
in real time. It captures frames from the drone's camera, processes the image to identify green regions,
and issues movement commands to align the object with the center of the frame.

Features:
- Real-time green object detection via HSV thresholding
- Automatic movement: left/right and up/down based on position offset
- Visual feedback via OpenCV windows
- Safe landing and resource cleanup on exit

Author: [Qiyue Chen]
Date: [2025-06-30]
"""

from djitellopy import Tello
import cv2
import numpy as np
import time

# ---------------------------------------------
# Drone Setup
# ---------------------------------------------

# Initialize the Tello drone
tello = Tello()
tello.connect()         # Establish connection
tello.streamon()        # Start video stream

# Take off and wait briefly for stabilization
tello.takeoff()
time.sleep(2)

# ---------------------------------------------
# Frame and Center Configuration
# ---------------------------------------------

# Define frame dimensions and center coordinates
frame_width = 640
frame_height = 480
center_x = frame_width // 2
center_y = frame_height // 2

# Define movement tolerance: drone won't move if object is near center
tolerance = 40  # pixels

# ---------------------------------------------
# Object Detection Function
# ---------------------------------------------

def find_green_object(frame):
    """
    Detect the largest green-colored object in a frame using HSV masking.

    Parameters:
        frame (np.array): BGR image from the drone camera

    Returns:
        tuple: (x, y) center coordinates of object or None if not found,
               binary mask used for detection
    """
    # Convert BGR image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define HSV thresholds for green color
    lower_green = np.array([40, 70, 70])
    upper_green = np.array([80, 255, 255])

    # Create a binary mask where green is white and other areas are black
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours from the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Choose the largest contour (assume it's the object)
        c = max(contours, key=cv2.contourArea)

        # Ignore small objects (noise)
        if cv2.contourArea(c) > 300:
            x, y, w, h = cv2.boundingRect(c)
            center = (x + w // 2, y + h // 2)
            return center, mask

    return None, mask

# ---------------------------------------------
# Main Tracking Loop
# ---------------------------------------------

try:
    while True:
        # Read the latest frame from the drone
        frame = tello.get_frame_read().frame

        # Resize for faster processing and consistent shape
        frame = cv2.resize(frame, (frame_width, frame_height))

        # Detect green object and get the binary mask
        center, mask = find_green_object(frame)

        if center:
            # Draw a green dot at the object center
            cv2.circle(frame, center, 10, (0, 255, 0), -1)

            # Calculate horizontal (X) and vertical (Y) error
            offset_x = center[0] - center_x
            offset_y = center_y - center[1]  # Invert Y because image origin is top-left

            # Adjust drone position based on X error (left/right)
            if offset_x < -tolerance:
                tello.move_left(20)
            elif offset_x > tolerance:
                tello.move_right(20)

            # Adjust drone position based on Y error (up/down)
            if offset_y > tolerance:
                tello.move_up(20)
            elif offset_y < -tolerance:
                tello.move_down(20)

        # Show the processed frames
        cv2.imshow("Tello Stream", frame)
        cv2.imshow("Mask", mask)

        # Quit the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# ---------------------------------------------
# Safe Exit
# ---------------------------------------------
finally:
    # Land the drone and clean up resources
    tello.land()
    tello.streamoff()
    cv2.destroyAllWindows()
