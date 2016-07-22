import numpy as np
import cv2
import glob



criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:7].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

###CHANGE: USE VIDEO CAPTURE (SEE STEP1)
cap = cv2.VideoCapture(0)
capture = False

while(True):
  
  key = cv2.waitKey(1)
  
  if key & 0xFF == 119:
    print("w")
    capture = True
  
  elif cv2.waitKey(1) & 0xFF == ord('q'):
    break

  # if cv2.waitKey(0) & 0xFF == 97:
  #   print("a")
  #   capture = False

  ret, img = cap.read()
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

  # Find the chess board corners
  ret, corners = cv2.findChessboardCorners(gray, (7,7),None)
  cv2.imshow('img',gray)

  # If found, add object points, image points (after refining them)
  if ret == True and capture:

      corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
      imgpoints.append(corners2.tolist())
      objpoints.append(objp)
      # Draw and display the corners
      
      img = cv2.drawChessboardCorners(img, (7,7), corners2,ret)
      cv2.imshow('img',img)
      cv2.waitKey(500)
      
      capture = False      

ret, img = cap.read()
shape = img.shape[:2]
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, shape[::-1],None, None)

cap.release()
cv2.destroyAllWindows()
