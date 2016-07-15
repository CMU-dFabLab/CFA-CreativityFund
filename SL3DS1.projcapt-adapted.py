import cv2
import numpy as np
import os

textvalcap = "C:\\Users\\Pedro\\Google Drive\\CMoA_Plaster\\SL - Python Implementation\\HHSL3DScanner\\"
###### 1 SETTING CAMERAS
video_capture0 = cv2.VideoCapture(0)
video_capture0.set(10, 30.0) #BRIGHTNESS
video_capture0.set(11, 5.0) #CONTRAST
video_capture0.set(12, 100.0) #SATURATION
video_capture0.set(15,-8.0) #EXPOSURE
video_capture0.set(17,10000.0) #WHITE_BALANCE
video_capture0.set(3,1920.0) #WIDTH
video_capture0.set(4,1080.0) #HEIGHT
video_capture1 = cv2.VideoCapture(1)
video_capture1.set(10, 30.0) #BRIGHTNESS
video_capture1.set(11, 5.0) #CONTRAST
video_capture1.set(12, 100.0) #SATURATION
video_capture1.set(15,-8.0) #EXPOSURE
video_capture1.set(17,10000.0) #WHITE_BALANCE
video_capture1.set(3,1920.0) #WIDTH
video_capture1.set(4,1080.0) #HEIGHT

###### 2 TESTING CAMERAS: SHOWING 2 FRAMES
ret, frame0 = video_capture0.read()
cv2.imshow("cam0", frame0)
ret, frame1 = video_capture1.read()
cv2.imshow("cam1", frame1)
cv2.waitKey(5000)

ret, frame0 = video_capture0.read()
cv2.imshow("cam0", frame0)
ret, frame1 = video_capture1.read()
cv2.imshow("cam1", frame1)
cv2.waitKey(5000)
cv2.destroyAllWindows()

###### 3 PRINTING PROPERTIES OF THE CAMERA
#for ii in range(0,19):
#    print (ii, video_capture0.get(ii))
## open a borderless window for showing projector images as a second display    

###### 4 SETTING WINDOW FOR STRUCTURED LIGHTING PATTERNS  
cv2.namedWindow("Projector Window", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Projector Window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_AUTOSIZE)
cv2.resizeWindow("Projector Window", 1024,768) #reset t 1024,768
#cv2.moveWindow("Projector Window", 1025, -2) #why?

###### 5 CREATING FOLDERS TO SAVE IMAGES FROM BOTH CAMERAS
try: os.makedirs(textvalcap +"CAMR")
except OSError: pass
try: os.makedirs(textvalcap + "CAML")
except OSError: pass

###### 6 LOADING NUMPY IMAGE (3D ARRAY OF 0s and 255s)
imggray=np.load('proj.npy')

###### 7 DISPLAYING AND CAPTURING SEQUENCE OF PATTERNS
for x in range(1, 43):
    cv2.imshow("Projector Window",imggray[:,:,x-1])
    filename0 = textvalcap + 'CAMR\\CAM0%02d.png'%(x,)
    filename1 = textvalcap + 'CAML\\CAM1%02d.png'%(x,)
    ret, frame0 = video_capture0.read()
    cv2.waitKey(100)
    ret, frame1 = video_capture1.read()
    cv2.waitKey(100)
    cv2.imwrite(filename0,frame0)
    cv2.imwrite(filename1,frame1)

####### 8 HOUSEKEEPING
video_capture0.release()
video_capture1.release()
cv2.destroyAllWindows()
