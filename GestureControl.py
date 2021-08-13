import mediapipe as mp
import cv2
import math


class handDetector():
    def __init__(self,mode=False,maxHands=2,detectCon=0.8,trackCon=0.5):
        self.mode = mode 
        self.maxHands = maxHands
        self.detectCon = detectCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,
                                        self.detectCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        
    def findHands(self,img,draw=True):
        
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        
        if self.results.multi_hand_landmarks:
            for self.handLmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,self.handLmarks,self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPos(self,img,handNo=0,draw=True):
        
        self.lmList = []
        xList = []
        yList = []
        bbox = []
        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for ID,lm in enumerate(myHand.landmark):
                h,w,c=img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                self.lmList.append([ID,cx,cy])
                xList.append(cx)
                yList.append(cy)
                if draw:
                    cv2.circle(img,(cx,cy),0,(255,0,255),cv2.FILLED)
                
            xmin,xmax = min(xList),max(xList)
            ymin,ymax = min(yList),max(yList)
            bbox = xmin,ymin,xmax,ymax
            
            if draw:
                cv2.rectangle(img,(bbox[0]-20,bbox[1]-20),
                              (bbox[2]+20,bbox[3]+20),(0,255,0),2)
        return self.lmList,bbox
    
    def pointDistance(self,p1,p2,img,draw=True):
        
        x1,y1 = self.lmList[p1][1],self.lmList[p1][2]
        x2,y2 = self.lmList[p2][1],self.lmList[p2][2]
        cx,cy = int((x1+x2)/2),int((y1+y2)/2)
        length = math.hypot(x1-x2,y1-y2)
        
        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),1)
            cv2.circle(img,(cx,cy),5,(0,0,255),cv2.FILLED)
        return length,img,[x1,y1,x2,y2,cx,cy]
    
    def fingersUp(self):
        fingers = []
        self.tipIds = [4,8,12,16,20]
        #Thumb
        if self.lmList[self.tipIds[0]][2] < self.lmList[self.tipIds[0]-1][2]:
            fingers.append(1)
        else:
            fingers.append(0)
        #Fingers
        for ID in range(1,5):
            if self.lmList[self.tipIds[ID]][2] < self.lmList[self.tipIds[ID]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers