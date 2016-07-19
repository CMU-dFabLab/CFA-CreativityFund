import numpy as np
import cv2
import os
import glob
import operator

def visualizeImage(img_name, img_title):
  """ visualize and print the values of a matrix/image """
  window_name = "test"
  cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
  cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, 
    cv2.WINDOW_AUTOSIZE)
  cv2.resizeWindow(window_name, 1280, 720)
  cv2.imshow(window_name, img_name)
  cv2.waitKey(10000)
  print("\n\n\n\n\n{} = ".format(img_title))
  #print middle row of the image
  row = [img_name[len(img_name)//2][i] for i in range(len(img_name[0]))]
  print (row)

def imageFrom3dmatrix(matrix, level):
  """ extract one layer (2d matrix) from a 3d matrix """ 
  #rcode = imageFrom3dmatrix(rightcamcode, 0)
  f = lambda x : x[level]
  return np.apply_along_axis(f, 2, matrix)


def createMask(threshold, firstImage):
  """ use first image of projections (white rectangle) to create shadow and outside areas mask"""
  img1=cv2.imread(firstImage,cv2.IMREAD_GRAYSCALE)
  ret,img1 = cv2.threshold(img1,threshold,255,cv2.THRESH_TOZERO)
  old_settings = np.seterr(all='ignore') #make sure  that errors will not prevent operations
  imgmask=np.divide(img1,img1)
  #in numpy versions 1.11.1+ division by 0 results in NaN... trick to solve it:
  imgmask = np.nan_to_num(imgmask)
  return imgmask

def getSortedUniqueColoc(horzlino, vertlino, Rcamcode, Lcamcode, imgmaskR, imgmaskL):
  """
  (Rcamcode and Lcamcode are 3d lists with 1024*768*2 elements from two cameras,
    imgmaskR and imgmaskL are masks for the unwanted areas around the images)
  find similar points in both camera based on projected patterns, 
  and save all the wanted pixel informations in lists
  """
  kkl, kkr = 0, 0 #variables to store number of valid pixels in each camera code
  colocright, colocleft=[], []
  rightsrt, leftsrt=[], []
  #traversing image, checking if pixel is valid and appending it to the lists
  for ii in range(0, horzlino):
      for jj in range(0, vertlino):
          if (rightcamcode[jj][ii][0]!=0 and rightcamcode[jj][ii][1]!=0 and imgmaskright[jj][ii]!=0):
             colocright.append(np.uint32([rightcamcode[jj][ii][0]+rightcamcode[jj][ii][1]*1024, ii, jj]))
             rightsrt.append(rightcamcode[jj][ii][0]+rightcamcode[jj][ii][1]*1024)
             kkl=kkl+1
          if (leftcamcode[jj][ii][0]!=0 and leftcamcode[jj][ii][1]!=0 and imgmaskleft[jj][ii]!=0):
             colocleft.append(np.uint32([leftcamcode[jj][ii][0]+leftcamcode[jj][ii][1]*1024,ii ,jj]))
             leftsrt.append(leftcamcode[jj][ii][0]+leftcamcode[jj][ii][1]*1024)
             kkr=kkr+1
  print (kkr,kkl)
  np.savetxt("leftcod" , colocleft ,fmt='%d', delimiter=', ', newline='\n')
  np.savetxt("rightcod" , colocright ,fmt='%d', delimiter=', ', newline='\n')
  
  #sorting
  colocrightsrt, colocleftsrt=[], []
  #sort according to the first element in coloc
  colocrightsrt=sorted(colocright, key=operator.itemgetter(0))
  colocleftsrt=sorted(colocleft, key=operator.itemgetter(0))
  rightsrtt=sorted(rightsrt)
  leftsrtt=sorted(leftsrt)
  #saving sorted [[value, LCx, LCy], [value, LCx, LCy], [value, LCx, LCy] ...] - allows repeated
  #saving sorted [value, value, value ...] - unique
  np.save("colocleftsrt" , colocleftsrt)
  newlistl=np.unique(leftsrtt) 
  np.savetxt("colocleftsrtuniq" , newlistl ,fmt='%d', delimiter=', ', newline='\n')
  np.save("colocrightsrt" , colocrightsrt)
  newlistr=np.unique(rightsrtt) 
  np.savetxt("colocrightsrtuniq" , newlistr ,fmt='%d', delimiter=', ', newline='\n')

  return (newlistr, newlistl, colocrightsrt, colocleftsrt, rightsrtt, leftsrtt)


def getMatchpixels(newlistr, newlistl, colocrightsrt, colocleftsrt, rightsrtt, leftsrtt):
  """finding common points in both cameras and storing its coordinates for 3d point cloud calculation"""
  #Return the sorted, unique values that are in both of the input arrays.
  camunio=np.intersect1d(newlistl,newlistr)
  kkr, kkl, kk=0, 0, 0
  matchpixels=np.zeros((np.size(camunio),4), dtype=np.int16)
  #for each unique value present in both right and left lists of pixels (camunio) 
  #find the first occurence in the original sorted list and store its coordinates  
  for i in camunio:
      #find position of first pixel with the value i
      while (rightsrtt[kkr] != i):
          kkr=kkr+1
      while (leftsrtt[kkl] != i):
          kkl=kkl+1
      #store its position in the matchpixel 2d list
      matchpixels[kk][0]=colocrightsrt[kkr][1]  # right camera x pixel coordinate
      matchpixels[kk][1]=colocrightsrt[kkr][2]  # right camera y pixel coordinate
      matchpixels[kk][2]=colocleftsrt[kkl][1]   #left camera x pixel coordinate
      matchpixels[kk][3]=colocleftsrt[kkl][2]   #left camera y pixel coordinate
      kk=kk+1

  np.savetxt("colocuniq" , matchpixels ,fmt='%d', delimiter=',', newline='\n')

  return matchpixels


horzlino=1280
vertlino=720
base_path = "T:\\Darcy\\COMA-PLASTER\\"
#loading color code (gray code) files from step 2 to map the coordinates
rightcamcode=np.load(base_path+"CAMR\\coloccod.npy" )
leftcamcode=np.load(base_path+"CAML\\coloccod.npy" )
#threshold
thresholdleft=np.load(base_path + "thresholdleft.npy" )
thresholdright=np.load(base_path + "thresholdright.npy" )
#firstImage
imgmaskrightf = base_path + "CAMR\\CAM001.png"
imgmaskleftf = base_path + "CAML\\CAM101.png"
#create masks
imgmaskleft=createMask(thresholdleft, imgmaskleftf)
imgmaskright=createMask(thresholdright, imgmaskrightf)
#visualizeImage(imgmaskleft, "imgmaskleft")
print("STEP 1: Mask done!")
newlistr, newlistl, colocrightsrt, colocleftsrt, rightsrtt, leftsrtt = getSortedUniqueColoc(horzlino, vertlino, 
  rightcamcode, leftcamcode, imgmaskright, imgmaskleft)
print ("STEP2: leftcod, rightcod, colocleftsrt, colocleftsrtuniq, colocrightsrt, colocrightsrtuniq sorted and saved!")
getMatchpixels(newlistr, newlistl, colocrightsrt, colocleftsrt, rightsrtt, leftsrtt)
print ("STEP 3: calcxy1xy2 Done!")
