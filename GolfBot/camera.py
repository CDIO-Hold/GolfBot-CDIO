import cv2
import numpy as np

from robot import Robot

cap = cv2.VideoCapture(0)

# Define the color range for detecting the ball for orange
lower_color = np.array([5, 150, 180])  # Lower bound of orange in HSV
upper_color = np.array([30, 255, 255])  # Upper bound of orange in HSV

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Display the HSV frame
    cv2.imshow('HSV Frame', hsv)

    # Create a mask using the color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Display the mask
    cv2.imshow('Mask', mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour and draw it
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
        if radius > 10:  # Adjust the threshold as needed
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)

            # Print or display the HSV values of the center pixel
            hsv_center = hsv[int(y), int(x)]
            print("HSV Values at center pixel:", hsv_center)

    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Break the loop when the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

def detectRobot():
    
    return robot


# Release the capture
cap.release()
cv2.destroyAllWindows()