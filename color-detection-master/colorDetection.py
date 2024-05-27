import cv2
from PIL import Image 
import numpy as np

ORANGE = {
    'lower': np.array([0,158,103]),
    'upper': np.array([27,202,158]) 
}

COLOR2 = {
    'lower': np.array([0,138,60]),
    'upper': np.array([20,255,160]) 
}

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    # frame dimension :  480 x 640

    # middle rectangle
    #xr1, yr1, xr2, yr2 = 160, 120, 480, 360
    #img = cv2.rectangle(frame, (xr1, yr1), (xr2, yr2), (255, 0,0), 2)

    
    #lines
    line1 = cv2.line(frame, (200, 0), (200, height), (255, 0, 0), 1)
    line2 = cv2.line(frame, (440, 0), (440, height), (255, 0, 0), 1)
    line3 = cv2.line(frame, (0, 180), (width, 180), (255, 0, 0), 1)
    line4 = cv2.line(frame, (0, 300), (width, 300), (255, 0, 0), 1)
    

    #convert BGR to HSV
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #mask video from lower to upper value
    track_color = COLOR2
    mask = cv2.inRange(hsvImage, track_color['lower'], track_color['upper'])
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        for contour in contours:
            if cv2.contourArea(contour) > 50:
                c = max(contours, key=cv2.contourArea)
                x1, y1, x2, y2 = cv2.boundingRect(c)
                w = x1 + x2
                h = y1 + y2
                frame = cv2.rectangle(frame,(x1,y1),(w,h),(255, 165, 0), 3)

                '''
                # if object in rectangle show 'IN' text

                if x1>=xr1 and y1>=yr1 and x2<=xr2 and y2<=yr2:
                    cv2.putText(frame, 'IN', (10, 380), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 0), 2)
                '''  

                xs1, ys1, xe1, ye1 = 200, 0, 200, height
                xs2, ys2, xe2, ye2 = 440, 0, 440, height
                xs3, ys3, xe3, ye3 = 0, 180, width, 180
                xs4, ys4, xe4, ye4 = 0, 300, width, 300

                cv2.putText(frame, 'Target Found', (10, 420), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

                # Target Passed (ganti posisi jadi kanan atas)
                if y1 > ys4:
                    cv2.putText(frame, 'Target Passed', (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

                # Going Right
                if w < xs1 and h < ys4:
                    cv2.putText(frame, 'Going Right', (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

                # Going Left
                if x1 > xs2 and h < ys4:
                    cv2.putText(frame, 'Going Left', (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

                # On Sight
                if x1 > xs1 and w < xs2 and h < ys3:
                    cv2.putText(frame, 'On Sight', (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)  

                # Dropping Package
                if x1 > xs1 and w < xs2 and y1 > ys3 and h < ys4 :
                    cv2.putText(frame, 'DROPPING PACKAGE', (x1, y1-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)                   

                '''
                #object position
                cv2.putTextframe,f'x pos: {intx1)}',(10, 400), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                cv2.putText(frame, f'x pos: {int(y1)}', (10, 420), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 0), 2)

                # atas
                if y1 > 300:
                    cv2.putText(frame, 'bawah', (60, 440), cv2.FONT_HERSHEY_PLAIN,
                    1, (0, 255, 0), 2)

                # bawah
                else:
                    cv2.putText(frame, 'atas', (60, 440), cv2.FONT_HERSHEY_PLAIN,
                    1, (0, 255, 0), 2)

                # kanan
                if x1 > 300:
                    cv2.putText(frame, 'kanan', (10, 440), cv2.FONT_HERSHEY_PLAIN,
                    1, (0, 255, 0), 2)

                # kiri 
                else:
                    cv2.putText(frame, 'kiri', (10, 440), cv2.FONT_HERSHEY_PLAIN,
                    1, (0, 255, 0), 2)
                '''

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()