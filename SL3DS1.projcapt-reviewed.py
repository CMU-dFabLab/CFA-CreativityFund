import cv2
import numpy as np
import os
import tkinter

def settingCameras(n, camera_settings):
  """SETTING CAMERAS"""
  video_captures = []
  for i in range(n):
    temp_capture = cv2.VideoCapture(i)
    for key in camera_settings:
      temp_capture.set(key, camera_settings[key])
    video_captures.append(temp_capture)
  return video_captures

def testingCameras(video_captures):
  """TESTING CAMERAS: SHOWING 2 FRAMES"""
  for i in range(len(video_captures)):
    ret, frame = video_captures[i].read()
    cv2.imshow("cam" + str(i), frame)
  cv2.waitKey(5000)
  cv2.destroyAllWindows()

def printingCameraProperties(video_captures, n_properties):
  """PRINTING PROPERTIES OF THE CAMERA"""
  for i in range(len(video_captures)):
    for j in range(n_properties):
      print (j, video_captures[i].get(j))    

def settingWindow(window_name, width, height):
  """SETTING WINDOW FOR STRUCTURED LIGHTING PATTERNS"""
  cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
  cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, 
    cv2.WINDOW_AUTOSIZE)
  cv2.resizeWindow(window_name, width, height)
  #cv2.moveWindow("Projector Window", 1025, -2) #why? 

def makeDir(path, n):
  """ 
  CREATING FOLDERS TO SAVE IMAGES FROM BOTH CAMERAS
  CAM0 is right camera
  CAM1 is left camera
  ...
  """
  for i in range(n):
    try: os.makedirs(path + "\\" + 'CAM' + str(i))
    except OSError: pass

def displayAndCaptureImages(video_captures, window_name, pattern_file_name, 
  n_patterns, base_path):
  """ DISPLAY AND CAPTURE ALL THE IMAGES OF THE PATTERNS """
  """
  LOADING NUMPY IMAGE (3D ARRAY OF 0s and 255s) - A STACK OF 42 GRAY CODE IMAGES
  2 solid color images to create a shadow mask
  20 interchangeably the column and its inverted sequence
  20 interchangeably the row and its inverted sequence
  """

  imggray=np.load(pattern_file_name)
  cv2.imshow(window_name, imggray[:,:,0])
  cv2.waitKey(1000)
  # DISPLAYING AND CAPTURING SEQUENCE OF PATTERNS
  
  for i in range(1, n_patterns + 1):
      cv2.imshow(window_name, imggray[:,:,i-1])
      filenameCamera = [[] for c in range(len(video_captures))]
      for j in range(len(video_captures)): 
        filenameCamera[j] = base_path + "CAM" + str(j) + "\\CAM0%02d.png"%(i-2,) 
        #i-2 is eliminating 2 first pictures
        ret, frame = video_captures[j].read()
        cv2.waitKey(100)
      for k in range(len(video_captures)):    
        cv2.imwrite(filenameCamera[k],frame)

  #take 2 last pictures 
  for i in range(n_patterns + 1, n_patterns + 3):
      for j in range(len(video_captures)): 
        filenameCamera[j] = base_path + "CAM" + str(j) + "\\CAM0%02d.png"%(i-2,) 
        #i-2 is eliminating 2 first pictures
        ret, frame = video_captures[j].read()
        cv2.waitKey(100)
      for k in range(len(video_captures)):    
        cv2.imwrite(filenameCamera[k],frame)

def houseKeeping(video_captures):
  """release all the cameras and destroy all windows"""
  for i in range(len(video_captures)):
    video_captures[i].release()

  cv2.destroyAllWindows() 

def main():


  #STEP 0: SETTING VARIABLES
  base_path = "C:\\Users\\Pedro\\Google Drive\\CMoA_Plaster\\SL - Python Implementation\\HHSL3DScanner\\"

  camera_settings = ({10: 30.0, 11: 5.0, 12: 100.0, 15: -8.0, 17: 10000.0, 
    3: 1920.0, 4: 1080.0})
  #BRIGHTNESS, CONTRAST, SATURATION, EXPOSURE, WHITE_BALANCE, WIDTH, HEIGHT
  n_properties = 19
  n_patterns = 42
  window_name = "Projector Window"
  n_cameras = 2
  camera_width = 1024
  camera_height = 768

  #STEP 1: CAPTURE AND TEST CAMERAS
  video_captures = settingCameras(n_cameras, camera_settings)
  #testingCameras(video_captures)
  #printingCameraProperties(video_captures, n_properties)
  
  
  #STEP 2: SETTING WINDOWS 
  settingWindow(window_name, camera_width, camera_height)

  #STEP 3: CAPTURE AND SAVE IMAGES FOR FUTURE ANALYSIS
  makeDir(base_path, n_cameras)
  displayAndCaptureImages(video_captures, "Projector Window", "proj.npy", 
    n_patterns, base_path)
  
  #STEP 4: CLEANING THE HOUSE 
  houseKeeping(video_captures)

main()

