import cv2
from PIL import Image
import numpy as np
from pymavlink import mavutil

# Initialize the MAVLink connection
connection_string = '/dev/ttyUSB0'  # Adjust as per your connection
baud_rate = 57600
master = mavutil.mavlink_connection(connection_string, baud=baud_rate)

def set_servo_pwm(servo_num, pwm_value):
    """Send command to move servo"""
    master.mav.command_long_send(
        master.target_system,
        master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,
        0,
        servo_num,    # Servo number (1-8)
        pwm_value,    # PWM value (1000-2000)
        0, 0, 0, 0, 0)

# Servo configuration (adjust according to your setup)
SERVO_LEFT = 1
SERVO_RIGHT = 2
PWM_CENTER = 1500
PWM_MIN = 1000
PWM_MAX = 2000

# Function to adjust servo positions
def adjust_servos(obj_center_x, obj_center_y, center_x, center_y):
    if obj_center_x < center_x - 50:
        pwm_left = PWM_CENTER + 100
        pwm_right = PWM_CENTER - 100
    elif obj_center_x > center_x + 50:
        pwm_left = PWM_CENTER - 100
        pwm_right = PWM_CENTER + 100
    else:
        pwm_left = PWM_CENTER
        pwm_right = PWM_CENTER
    
    set_servo_pwm(SERVO_LEFT, pwm_left)
    set_servo_pwm(SERVO_RIGHT, pwm_right)

# Object detection and tracking
ORANGE = {'lower': np.array([0, 91, 155]), 'upper': np.array([25, 195, 207])}
COLOR2 = {'lower': np.array([0, 91, 155]), 'upper': np.array([20, 195, 207])}
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

    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    frame = adjust_contrast_brightness(frame, contrast=1.5, brightness=10)

    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    frame = cv2.filter2D(frame, -1, kernel)

    line1 = cv2.line(frame, (200, 0), (200, height), (255, 0, 0), 1)
    line2 = cv2.line(frame, (440, 0), (440, height), (255, 0, 0), 1)
    line3 = cv2.line(frame, (0, 180), (width, 180), (255, 0, 0), 1)
    line4 = cv2.line(frame, (0, 300), (width, 300), (255, 0, 0), 1)

    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
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

                # Adjust servos based on object position
                adjust_servos(obj_center_x, obj_center_y, center_x, center_y)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
