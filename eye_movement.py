from __future__ import division
from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
import pyautogui
import imutils
import math
import time
import dlib 
import cv2
import subprocess

val = 0
def mouse_movement_ctypes(angle):     
    global val
    if((angle==1)and(not(val == 1))):
        print("notepad - left")
        subprocess.Popen('C:\\Windows\\System32\\notepad.exe')
        val = val - val +1
    elif((angle==2)and(not(val == 2))):
        print("calc - right")
        subprocess.Popen('C:\\Windows\\System32\\calc.exe')
        val = val - val +2
    elif((angle==3)and(not(val == 3))):
        print("freecam - up")
        subprocess.Popen('C:\\Program Files (x86)\\Free Cam 8\\freecam.exe')
        val = val - val +3
    elif((angle==4)and(not(val == 4))):
        print("wmplayer - down")
        subprocess.Popen('C:\\Program Files (x86)\\Windows Media Player\\wmplayer.exe')
        val = val - val +4        
    elif(angle==0) :
        val = val - val +0   
    time.sleep(.5)
def mid_point(pt1,pt2):
    x = int((pt1[0]+pt2[0])/2)
    y = int((pt1[1]+pt2[1])/2)
    return x,y
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) 
    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]
    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')
    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y
def angle_two_points(p1,p2):
       m=(p2[1]-p1[1])/(p2[0]-p1[0])  
       a = (p2[1]-p1[1])
       b = (p2[0]-p1[0])        
       return math.degrees(math.atan(m))
def midpoint_of_eye(eye):
    top_eye = mid_point(eye[1],eye[2])
    bot_eye = mid_point(eye[4],eye[5])
    return line_intersection((top_eye,bot_eye),(eye[0],eye[3]))
def movement_face(angle,le,re):
    ea = (le+re)/2
    if(angle>10):
       mouse_movement_ctypes(1) 
    elif(angle<-10):
       mouse_movement_ctypes(2)  
    elif(ea>0.4):
       mouse_movement_ctypes(3)     
    elif(ea<0.25):
       mouse_movement_ctypes(4)     
    else:
       mouse_movement_ctypes(0)  
def eye_aspect_ratio(eye):    
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
time.sleep(1.0)
def recognize_face(frame):
    rects = detector(gray, 0)
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        left_p = midpoint_of_eye(leftEye)
        right_p = midpoint_of_eye(rightEye)
        movement_face(angle_two_points(right_p,left_p),leftEAR,rightEAR)
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
    return frame
while True:
    frame = cap.read()
    frame = frame[1]
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = recognize_face(frame)
    cv2.imshow("Frame", cv2.flip(frame,1))
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()