import torch
import cv2
import time

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='path/to/your/custom-trained-model.pt')

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to a format compatible with YOLOv5
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform inference
    results = model(img)

    # Render results on the frame
    results.render()

    # Convert the image back to BGR for OpenCV
    frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Display the resulting frame
    cv2.imshow('YOLOv5 Object Detection', frame)

    # Exit the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
