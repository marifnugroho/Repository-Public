import torch
import cv2

# Load the custom-trained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='path/to/your/custom-trained-model.pt')

# Initialize the video capture object
cap = cv2.VideoCapture(0)  # 0 is the default camera

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform inference on the frame
    results = model(frame)

    # Render the results on the frame
    frame = results.render()[0]

    # Display the frame
    cv2.imshow('YOLOv5 Detection', frame)

    # Break the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
