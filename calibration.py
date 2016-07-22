import numpy as np
import cv2
import glob


def settingCamera(camSettings):
  """SETTING CAMERA"""
  videoCapture = cv2.VideoCapture(0)
  for key in camSettings:
    videoCapture.set(key, camSettings[key])
  return videoCapture

camWidth, camHeight = 1024.0, 768.0
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
rowPts = 7
colPts = 7
squareSide = 20.8
camSettings = ({10: 30.0, 11: 5.0, 12: 100.0, 15: -8.0, 17: 10000.0, 
    3: camWidth, 4: camHeight})
n_properties = 19

#EXPECTED VALUES
#pixelSize = 0.0043 #mm
#focalLength = 18 #mm
#pixelsPerMm = 232.55813953488372093023255813953 #1/pixelSize9


videoCapture = settingCamera(camSettings)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((rowPts*colPts,3), np.float32)
objp[:,:2] = np.mgrid[0:rowPts*squareSide:squareSide,0:colPts*squareSide:squareSide].T.reshape(-1,2)

print(objp)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

capture = False
"""
while(True):
  key = cv2.waitKey(1) 

  if key & 0xFF == 119:
    print("w")
    capture = True

  elif key & 0xFF == ord('q'):
    break

  ret, img = videoCapture.read()
  #ret, img = cap.read()
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

  # Find the chess board corners
  ret, corners = cv2.findChessboardCorners(gray, (7,7),None)
  cv2.imshow('img',gray)

  # If found, add object points, image points (after refining them)
  if ret == True and capture:

      corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
      imgpoints.append(corners2)
      objpoints.append(objp)
      # Draw and display the corners
      
      img = cv2.drawChessboardCorners(img, (7,7), corners2,ret)
      cv2.imshow('img',img)
      cv2.waitKey(500)
      
      capture = False      

#ret, img = cap.read()
ret, img = videoCapture.read()
shape = img.shape[:2]
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, shape[::-1],None, None)
print (mtx)
print (mtx.tolist())
"""
videoCapture.release()
cv2.destroyAllWindows()

