import numpy as np
import cv2
import os
import glob
import operator

def visualizeImage(img_name, img_title):
  window_name = "test"
  cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
  cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, 
    cv2.WINDOW_AUTOSIZE)
  cv2.resizeWindow(window_name, 1280, 720)
  visualize(window_name, img_name, img_title)

def visualize(window_name, img_name, img_title):
  cv2.imshow(window_name, img_name) #this will show everything in 0 or 1
  cv2.waitKey(10000)
  print("\n\n\n\n\n{} = ".format(img_title))
  row = [img_name[len(img_name)//2][i] for i in range(len(img_name[0]))]
  print (row)

def imageFrom3dmatrix(matrix, level):
  #rcode = imageFrom3dmatrix(rightcamcode, 0)
  f = lambda x : x[level]
  return np.apply_along_axis(f, 2, matrix)


def createMask(threshold, firstImage):
  img1=cv2.imread(firstImage,cv2.IMREAD_GRAYSCALE)
  ret,img1 = cv2.threshold(img1,threshold,255,cv2.THRESH_TOZERO)
  imgmask=np.divide(img1,img1)
  return imgmask




def getSortedUniqueColoc(horzlino, vertlino, Rcamcode, Lcamcode, imgmaskR, imgmaskL):
  """
  (Rcamcode and Lcamcode are 3d lists with 1024*768*2 elements from two cameras,
    imgmaskR and imgmaskL are masks for the unwanted areas around the images)
  find similar points in both camera based on projected patterns, 
  and save all the wanted pixel informations in lists
  """
  kkl, kkr = 0, 0
  colocright, colocleft=[], []
  rightsrt, leftsrt=[], []
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
  """
  print(colocright[0:10])
  print("\n",colocleft[0:10])
  print("\n\n\n\n",colocrightsrt[0:10])
  print("\n",colocleftsrt[0:10])
  """
  #saving sorted [[value, LCx, LCy], [value, LCx, LCy], [value, LCx, LCy] ...] - allows repeated
  #saving sorted [value, value, value ...] - unique
  np.save("colocleftsrt" , colocleftsrt)
  newlistl=np.unique(leftsrtt) 
  np.savetxt("colocleftsrtuniq" , newlistl ,fmt='%d', delimiter=', ', newline='\n')
  np.save("colocrightsrt" , colocrightsrt)
  newlistr=np.unique(rightsrtt) 
  np.savetxt("colocrightsrtuniq" , newlistr ,fmt='%d', delimiter=', ', newline='\n')

  return (newlistr, newlistl, colocrightsrt, colocleftsrt)


def getMatchpixels(newlistr, newlistl, colocrightsrt, colocleftsrt):
  #finding common points in both cameras
  #Return the sorted, unique values that are in both of the input arrays.
  camunio=np.intersect1d(newlistl,newlistr)
  print(len(camunio), camunio, "\n\n\n")
  kkr, kkl, kk=0, 0, 0
  matchpixels=np.zeros((np.size(camunio),4), dtype=np.int16)
  print(matchpixels, "\n\n\n")
  #matchpixels[kk][0], matchpixels[kk][1], matchpixels[kk][2], matchpixels[kk][3] = 0, 0, 0, 0
  """
  I don't understand yet the logic of the while loop... it seems the opposite of what I would do.
  It is using a unique list of intersected values to find out the coordinates first pixel with that value
  in each camera to fill the arrays cited above. This is going to take all the crazy parallel arrays and 
  it is going to generate a list of arrays of 4 elements: [CRx, CRy, CLx, CLy].
  """
  for i in camunio:
      while (rightsrtt[kkr] != i):
          kkr=kkr+1
          matchpixels[kk][0]=colocrightsrt[kkr][1]  # right camera x pixel coordinate
          matchpixels[kk][1]=colocrightsrt[kkr][2]  # right camera y pixel coordinate
      while (leftsrtt[kkl] != i):
          kkl=kkl+1
          matchpixels[kk][2]=colocleftsrt[kkl][1]   #left camera x pixel coordinate
          matchpixels[kk][3]=colocleftsrt[kkl][2]   #left camera y pixel coordinate
      kk=kk+1

  np.savetxt("colocuniq" , matchpixels ,fmt='%d', delimiter=',', newline='\n')
  return matchpixels



old_settings = np.seterr(all='ignore')

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
print("Mask done!")
newlistr, newlistl, colocrightsrt, colocleftsrt = getSortedUniqueColoc(horzlino, vertlino, 
  rightcamcode, leftcamcode, imgmaskright, imgmaskleft)
print ("leftcod, rightcod, colocleftsrt, colocleftsrtuniq, colocrightsrt, colocrightsrtuniq saved!")
#sortColocAndSrt(colocright, colocleft, rightsrt, leftsrt)
#print ("sorted and saved!")
getMatchpixels(newlistr, newlistl, colocrightsrt, colocleftsrt)
print ('calcxy1xy2 Done!')
