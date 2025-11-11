import numpy as np
import cv2
import os

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the paths to the XML files
face_cascade_path = os.path.join(BASE_DIR, 'haarcascade_frontalface_default.xml')
eye_cascade_path = os.path.join(BASE_DIR, 'haarcascade_eye.xml')

face_cascade = cv2.CascadeClassifier(face_cascade_path)
eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

def capture(path):
    try:
        result = []
        cap = cv2.VideoCapture(path)
        while(cap.isOpened()):
            ret, img = cap.read()
            if ret:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    roi_gray = gray[y:y + h, x:x + w]
                    roi_color = img[y:y + h, x:x + w]
                    eyes = eye_cascade.detectMultiScale(roi_gray,minNeighbors=15)
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                        if (eyes & faces).any():
                            result.append(True)

                # cv2.imshow('frame', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        cap.release()
        cv2.destroyAllWindows()
        if any(result):
            return True, "Success!"
        else:
            return False, "KYC Failed! No Face detected!"
    except Exception as e:
        print(e)
        return False, "KYC unsuccess!"