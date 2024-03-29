import cv2
import numpy as np


def detect_ping_pong_balls(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # Detect edges using Canny edge detector
    edges = cv2.Canny(blurred, 50, 150)

    # Apply Hough Circle Transform to detect circles
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=1, minDist=20,
                               param1=50, param2=30, minRadius=5, maxRadius=30)

    detected_image = image.copy()

    ball_coords = []
    # Draw detected circles
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(detected_image, (x, y), r, (0, 255, 0), 4)
            ball_coords.append((x, y))

    return detected_image, ball_coords


# Capture video from webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    if not ret:
        break

    # Detect ping pong balls and coords
    detected_frame, ball_coords = detect_ping_pong_balls(frame)

    # Display the frame with ping pong balls detected
    cv2.imshow('Ping Pong Ball Detection', detected_frame)
    if ball_coords is not None:
        print('Ping Pong Ball Detection at', ball_coords)
        
    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()
