import cv2
import numpy as np

ORANGE = {
    'lower': np.array([0, 91, 155]),
    'upper': np.array([25, 195, 207])
}

COLOR2 = {
    'lower': np.array([0, 91, 155]),
    'upper': np.array([20, 195, 207])
}

def adjust_contrast_brightness(image, contrast=1.0, brightness=0):
    """Adjust contrast and brightness of an image."""
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

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

    # Draw reference lines
    cv2.line(frame, (200, 0), (200, height), (255, 0, 0), 1)
    cv2.line(frame, (440, 0), (440, height), (255, 0, 0), 1)
    cv2.line(frame, (0, 180), (width, 180), (255, 0, 0), 1)
    cv2.line(frame, (0, 300), (width, 300), (255, 0, 0), 1)
    cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)  # Draw the center point

    # Convert BGR to HSV
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mask the image
    mask = cv2.inRange(hsvImage, COLOR2['lower'], COLOR2['upper'])
    contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > 50:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 165, 0), 3)
            obj_center_x = x + w // 2
            obj_center_y = y + h // 2

            # Draw the object's center point
            cv2.circle(frame, (obj_center_x, obj_center_y), 5, (0, 255, 255), -1)

            # Provide instructions based on the object's position
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

            # Additional instructions based on position in quadrants
            if obj_center_y > 300:
                cv2.putText(frame, 'Target Passed', (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
            elif x + w < 200:
                cv2.putText(frame, 'Going Right', (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
            elif x > 440:
                cv2.putText(frame, 'Going Left', (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
            elif x > 200 and x + w < 440 and y + h < 180:
                cv2.putText(frame, 'On Sight', (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
            elif x > 200 and x + w < 440 and y > 180 and y + h < 300:
                cv2.putText(frame, 'DROPPING PACKAGE', (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
