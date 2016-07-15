import numpy as np
import cv2
import os
import glob

#variables
horzlino=1920
vertlino=1080
base_path = "T:\\Darcy\\COMA-PLASTER\\"
temp_path = base_path + "CAML"+ "\\"

left_img_names = glob.glob(temp_path + "*.png")
imgleft=cv2.imread(left_img_names[0],cv2.IMREAD_GRAYSCALE)

ii=50

def getBestThreshold(ii, img):
    """
    adjusting the threshold for processing area and eliminating shadows
    use left and right arrow key to adjust and press 'q' when finished
    """
    while True:
        ret,img1th = cv2.threshold(img,ii,255,cv2.THRESH_TOZERO)
        cv2.putText(img1th,"Threshold is "+str(ii), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 2, 255)
        cv2.imshow("PWindow2",img1th)
        k = cv2.waitKey(0)  
        if k == 113:#press q
            break
        elif k == 2555904: #press right
            ii=ii+1
        elif k == 2424832: #press left
            ii=ii-1
    cv2.destroyAllWindows()
    return ii

iiLeft = getBestThreshold(ii, imgleft)
np.save(base_path + "\\thresholdleft" , iiLeft)
    
temp_path = base_path + "CAMR" + "\\"
right_img_names = glob.glob(temp_path + "*.png")
imgRight=cv2.imread(right_img_names[0],cv2.IMREAD_GRAYSCALE)

iiRight = getBestThreshold(iiLeft, imgRight)
np.save(base_path + "thresholdright" , iiRight)
print ('Threshold Done!')
