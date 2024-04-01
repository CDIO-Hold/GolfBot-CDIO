import cv2
import cvzone
import numpy as np
from cvzone.ColorModule import ColorFinder


def calculate_circularity(contour):
    """
    Calculate circularity of a contour.

    Args:
        contour: Contour for which circularity needs to be calculated.

    Returns:
        Circularity value.
    """
    area = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    circularity = 4 * np.pi * area / (perimeter * perimeter)
    return circularity


def filter_circular_contours(contours, threshold=0.2):
    """
    Filter contours based on circularity.

    Args:
        contours: List of contours to be filtered.
        threshold: Circularity threshold for filtering (default is 0.2).

    Returns:
        Filtered list of contours.
    """
    filtered_contours = []
    for contour in contours:
        circularity = calculate_circularity(contour['cnt'])
        if circularity > threshold:
            filtered_contours.append(contour)
            print(round(circularity, 2))
    return filtered_contours


def capture_video(camera_index=2, width=1280, height=720):
    """
    Capture video from the specified camera.

    Args:
        camera_index: Index of the camera to use (default is 2).
        width: Width of the video capture (default is 1280).
        height: Height of the video capture (default is 720).

    Returns:
        Video capture object.
    """
    cap = cv2.VideoCapture(camera_index)
    cap.set(3, width)
    cap.set(4, height)
    return cap


class Ball:
    def __init__(self, name, hsv_color):
        self.name = name
        self.hsv_color = hsv_color


def process_frame(frame, color_finder, balls: list):
    """
    Process a single frame to detect circular objects.

    Args:
        frame: Input frame to process.
        color_finder: Color finder object for debugging.
        balls: List of Ball objects representing balls to detect.

    Returns:
        Processed frame with circular objects highlighted.
    """
    # img_color, mask = color_finder.update(frame, balls[0].hsv_color)
    # img_contour, contours = cvzone.findContours(frame, mask, filter=[4, 5, 6, 7, 8])
    # circular_contours = filter_circular_contours(contours)
    img_color_accum, mask_accum, img_contour_accum = frame.copy(), None, None
    
    for ball in balls:
        ball_img_color, ball_mask = color_finder.update(frame, ball.hsv_color)
        ball_img_contour, contours = cvzone.findContours(frame, ball_mask, filter=[4, 5, 6, 7, 8])

        circular_contours = filter_circular_contours(contours)

        for contour in circular_contours:
            # cv2.drawContours(img_color, [contour['cnt']], -1, (0, 255, 0), 3)
            # Draw rectangle around the contour
            x, y, w, h = contour['bbox']
            cv2.rectangle(ball_img_color, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # Add text indicating ball's name
            cv2.putText(ball_img_color, ball.name, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
      
        # Accumulate images for each ball
        img_color_accum = cv2.addWeighted(img_color_accum, 1, ball_img_color, 1, 0)
        if mask_accum is None:
            mask_accum = ball_mask
        else:
            mask_accum = cv2.bitwise_or(mask_accum, ball_mask)
        if img_contour_accum is None:
            img_contour_accum = ball_img_contour
        else:
            img_contour_accum = cv2.addWeighted(img_contour_accum, 1, ball_img_contour, 1, 0)

    return img_color_accum, mask_accum, img_contour_accum


def display_result(stack_images):
    """
    Display the result by stacking images and showing them in a window.

    Args:
        stack_images: List of images to stack for display.
    """
    img_stack = cvzone.stackImages(stack_images, 2, 0.5)
    cv2.imshow('Image', img_stack)
    cv2.waitKey(1)


def main():
    """
    Main function to capture video, process frames, and display the result.
    """
    cap = capture_video()
    my_color_finder = ColorFinder(False)

    white = {'hmin': 0, 'smin': 0, 'vmin': 16, 'hmax': 172, 'smax': 191, 'vmax': 152}
    white_ball = Ball("whiteBall", white)
    
    blue = {'hmin': 100, 'smin': 126, 'vmin': 11, 'hmax': 123, 'smax': 238, 'vmax': 51}
    blue_ball = Ball("blueBall", blue)
    
    balls = [white_ball, blue_ball]

    while True:
        success, frame = cap.read()
        if not success:
            break

        img_color, mask, img_contour = process_frame(frame, my_color_finder, balls)
        display_result([frame, img_color, mask, img_contour])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
