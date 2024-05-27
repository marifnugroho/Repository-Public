import cv2
from PIL import Image 
import numpy as np

ORANGE = {
    'lower': np.array([0, 91, 155]),
    'upper': np.array([25, 195, 207])
}

COLOR2 = {
    'lower': np.array([0, 91, 155]),
    'upper': np.array([20, 195, 207])
}

cap = cv2.VideoCapture(0)

def adjust_contrast_brightness(image, contrast=1.0, brightness=0):
    """Adjust contrast and brightness of an image."""
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))
    center_x = width // 2
    center_y = height // 2
    
    # Apply Gaussian Blur to reduce noise
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # Adjust contrast and brightness
    frame = adjust_contrast_brightness(frame, contrast=1.5, brightness=10)

    # Sharpen the image
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    frame = cv2.filter2D(frame, -1, kernel)

    # Draw lines
    line1 = cv2.line(frame, (200, 0), (200, height), (255, 0, 0), 1)
    line2 = cv2.line(frame, (440, 0), (440, height), (255, 0, 0), 1)
    line3 = cv2.line(frame, (0, 180), (width, 180), (255, 0, 0), 1)
    line4 = cv2.line(frame, (0, 300), (width, 300), (255, 0, 0), 1)

    # Convert BGR to HSV
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mask video from lower to upper value
    track_color = COLOR2
    mask = cv2.inRange(hsvImage, track_color['lower'], track_color['upper'])
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 50:
                c = max(contours, key=cv2.contourArea)
                x1, y1, w, h = cv2.boundingRect(c)
                x2 = x1 + w
                y2 = y1 + h
                frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 165, 0), 3)

                xs1, ys1, xe1, ye1 = 200, 0, 200, height
                xs2, ys2, xe2, ye2 = 440, 0, 440, height
                xs3, ys3, xe3, ye3 = 0, 180, width, 180
                xs4, ys4, xe4, ye4 = 0, 300, width, 300

                cv2.putText(frame, 'Target Found', (10, 420), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

                # Track object and provide instructions
                obj_center_x = x1 + w // 2
                obj_center_y = y1 + h // 2

                if obj_center_x < center_x - 50:
                    cv2.putText(frame, 'Move Right', (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                elif obj_center_x > center_x + 50:
                    cv2.putText(frame, 'Move Left', (10, 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                if obj_center_y < center_y - 50:
                    cv2.putText(frame, 'Move Down', (10, 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                elif obj_center_y > center_y + 50:
                    cv2.putText(frame, 'Move Up', (10, 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                if abs(obj_center_x - center_x) <= 50 and abs(obj_center_y - center_y) <= 50:
                    cv2.putText(frame, 'Centered', (10, 90), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

                # Additional conditions (maintaining existing code logic)
                if y1 > ys4:
                    cv2.putText(frame, 'Target Passed', (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

                if x1 < xs1 and h < ys4:
                    cv2.putText(frame, 'Going Right', (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

                if x1 > xs2 and h < ys4:
                    cv2.putText(frame, 'Going Left', (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

                if x1 > xs1 and x2 < xs2 and y1 < ys3:
                    cv2.putText(frame, 'On Sight', (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

                if x1 > xs1 and x2 < xs2 and y1 > ys3 and y2 < ys4:
                    cv2.putText(frame, 'DROPPING PACKAGE', (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

    cv2.imshow('frame', frame)
    # cv2.imshow('mask', mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
