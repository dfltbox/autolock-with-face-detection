import cv2
import threading
import time
import ctypes


#Logs a bunch of stuff to console if enabled
debug = True
#Amount of seconds until it locks when idle
locktime = 20
#Stops drawing rectangles over recognized faces if enabled
dontdraw = False
#Disables face recognition window if enabled
nowindow = False
#Reduces cpu usage of the program but will reduce fps if enabled
batterysaver = False


#DO NOT TOUCH
doidie = False
facewasdetected = False


def checkface():
    count = 0
    for i in range(locktime + 1):
        time.sleep(1)
        global doidie
        if(facewasdetected or doidie): 
            break
        if(count == locktime):
            ctypes.windll.user32.LockWorkStation()
            doidie = True
        else:
            count += 1
            if(debug):
                print(f'time until lock: ${count}')


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


cap = cv2.VideoCapture(0)

while True:
    if(batterysaver):
        time.sleep(0.35)
    if(doidie):
        break
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if(str(faces) == "()"):
        facewasdetected = False
        if(debug):
            print("no face detected!")
        threadcount = threading.active_count()
        #print(threadcount)
        if threadcount == 1:
            if(debug):
                print('starting thread')
            x = threading.Thread(target=checkface)
            x.start()

    else:
        if(debug):
            print(faces)
        facewasdetected = True

    if(dontdraw == False):
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    if(nowindow == False):
        cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        doidie = True
        break


cap.release()
cv2.destroyAllWindows()