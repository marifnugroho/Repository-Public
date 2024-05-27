import cv2 

for i in range (10):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Kamera ditemukan di index {i}")
        cap.release()
    else:
        print(f"kamera tidak ditemukan di index {i}")