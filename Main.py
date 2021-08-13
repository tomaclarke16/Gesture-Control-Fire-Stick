import numpy as np 
import cv2
import time
import keyboard
import FireStickController as fsc
import GestureControl as gs

fireStickIP = ""

def attentionDetect(landmarks):
    keyLandmarksX = {'tipsX':[8,12,16,20],'palmX':[4,9,13,17],'extra':[4,5,0]}
    
    keyLandmarksY = {'thumbY':[0,1,2,3,4],'indexY':[5,6,7,8],'middleY':[9,10,11,12],
                    'ringY':[13,14,15,16],'pinkyY':[17,18,19,20],'palmY':[0,17,9]
                    }
    
    conditions = []
    for x in keyLandmarksY.keys():
        y_coords = [landmarks[i][2] for i in keyLandmarksY[x]]
        for i in range(1,len(y_coords)):
            if y_coords[i]<y_coords[i-1]:
                conditions.append(True)
            else:
                conditions.append(False)
    for x in keyLandmarksX.keys():
        x_coords = [landmarks[i][1] for i in keyLandmarksX[x]]
        for i in range(1,len(x_coords)):
            if x_coords[i]>x_coords[i-1]:
                conditions.append(True)
            else:
                conditions.append(False)
    return all(conditions)  

def main():
    pTime,cTime = 0,0
    cap = cv2.VideoCapture(0)
    wCam,hCam = 1080,640
    cap.set(3,wCam)
    cap.set(4,hCam)

    detector = gs.handDetector()
    fireStick = fsc.FireStickController()
    fireStick.addDevice(fireStickIP)

    detect = True
    attention = False
    area = 0

    while True:
        success,img = cap.read()
        img = cv2.flip(img,flipCode=1)
        cTime = time.time()
        fps = int(1/(cTime-pTime))
        pTime = cTime
        cv2.putText(img,str(fps),(40,40),cv2.FONT_HERSHEY_PLAIN,
                    2,(255,0,0),3)
        
        img = detector.findHands(img)
        lmList,bbox = detector.findPos(img,draw=True)

        if len(lmList)!=0:
            attention = attentionDetect(lmList)
            cv2.putText(img,f"Attention: {attention}",(200,40),cv2.FONT_HERSHEY_PLAIN,
                        2,(255,0,0),3)

            #Gesture Functions
            if detect:
                #Go To Home
                if detector.fingersUp()==[1,1,1,1,0]:
                    detect = False
                    fireStick.home()
                #Play/Pause Control
                if detector.fingersUp()==[1,0,1,1,1]:
                    detect = False
                    fireStick.playPause()
                #Select Control
                if detector.fingersUp()==[1,1,0,1,1]:
                    detect = False
                    fireStick.select()
                #Back Control
                if detector.fingersUp()==[1,1,1,0,1]:
                    detect = False
                    fireStick.back()


            #Reset Detection
            if attention:
                detect = True
            else:
                detect = False

        cv2.imshow('Feed',img)
        cv2.waitKey(1)
        if keyboard.is_pressed('m'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
