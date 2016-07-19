import numpy as np
import cv2
import math
import csv


def RotateAndTranslate( x, y, z, pxpy, i, fc, ccdd, tet, phi):
    x1, y1, z1 = -(pxpy[i]-960)*fc, (pxpy[i+1]-540)*fc, ccdd
    alfa, beta = tet, phi
    gama = 0  
    #rotation about z axis
    Rright = np.array([[math.cos(gama), -math.sin(gama), 0],
                       [math.sin(gama),  math.cos(gama), 0],
                       [             0,               0, 1]])
    #rotation about x axis
    Rright = Rright.dot(np.array([[ 1,             0,               0], 
                                  [ 0,math.cos(beta), -math.sin(beta)] , 
                                  [ 0,math.sin(beta),  math.cos(beta)]]))
    #rotation about y axis
    Rright = Rright.dot(np.array([[math.cos(alfa), 0,-math.sin(alfa)], 
                                  [             0, 1,              0], 
                                  [math.sin(alfa), 0, math.cos(alfa)]])) 
    #rotation and translation
    XA = np.array(Rright.dot(([[x1],[y1],[z1]]))+([[x],[y],[z]]))
    #result for camera 1
    x1, y1, z1 = XA[0], XA[1], XA[2]   
    return (x1, y1, z1)


def camxyzparam(pxpy):
    ##################################################### function for calculating X,Y, and Z of points   
    fcr, fcl = 0.00269816, 0.00269816   #pixel size Focal Length for both cameras
    tetl = 0.26179938779914943653855361527329     #left camera rotation angle around Y axis (15 deg)
    tetr = -0.26179938779914943653855361527329    #right camera rotation angle
    phir, phil = 0, 0     #rotation angle around X axis 
    x0r, x0l = -250, 250     #translation in X direction
    y0r, y0l = 0, 0      #translation in Y direction
    z0r, z0l = 0, 0    
    ccddr, ccddl = 3.67, 3.67    #focal lenght for both cameras mm
    ###################################################
    x0, y0, z0 = x0r, y0r, z0r 
    x1, y1, z1 = RotateAndTranslate(x0, y0, z0, pxpy, 0, fcr, ccddr, tetr, phir)
    x2, y2, z2 = x0l, y0l, z0l
    x3, y3, z3 = RotateAndTranslate(x2, y2, z2, pxpy, 2, fcl, ccddl, tetl, phil)

    u = [float(x1)-x0, float(y1)-y0, float(z1)-z0]
    v = [float(x3-x2), float(y3-y2), float(z3-z2)]
    p = [x0,y0,z0]
    q = [x2,y2,z2]
    w = np.subtract(p,q)
    denomst = np.inner(v,u) * np.inner(v,u) - np.inner(v,v) * np.inner(u,u)
    s = (np.inner(w,u) * np.inner(v,v) - np.inner(v,u) * np.inner(w,v)) / denomst
    t = (np.inner(v,u) * np.inner(w,u) - np.inner(u,u) * np.inner(w,v)) / denomst
    xyz = np.divide((np.add(p,np.multiply(s,u)) + np.add(q,np.multiply(t,v))),2)
    abdist = np.add(p,np.multiply(s,u)) - np.add(q,np.multiply(t,v)) 
    return xyz,abdist





#==================================================================
ii = 0
rightcod = []
with open('rightcod', 'rt') as csvfile:
     xyreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in xyreader:
         rightcod.append([int(row[0]),int(row[1]),int(row[2])])

a = np.array(rightcod)
aa = a[a[:,0].argsort(),]
aaa, right_idx = np.unique(aa[:,0],return_index=True)

m = aaa.size
print ('Total points from right camera= ',m)
rightcodmean = np.zeros([m,3])

for ii in range(0,m-1):
    rightcodmean[ii]=[aaa[ii],np.mean(aa[right_idx[ii]:right_idx[ii+1],1]),np.mean(aa[right_idx[ii]:right_idx[ii+1],2])]

csvfile.close()
#==================================================================
ii = 0
leftcod=[]
with open('leftcod', 'rt') as csvfile:
     xyreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in xyreader:
         leftcod.append([int(row[0]),int(row[1]),int(row[2])])

a = np.array(leftcod)
aa=a[a[:,0].argsort(),]
aaa, left_idx=np.unique(aa[:,0],return_index=True)

m=aaa.size
print ('Total points left= ',m)
leftcodmean=np.zeros([m,3])

for ii in range(0,m - 1):
    leftcodmean[ii] = [aaa[ii], 
                       np.mean(aa[left_idx[ii]:left_idx[ii+1],1]), 
                       np.mean(aa[left_idx[ii]:left_idx[ii+1],2])]

codes = np.append(rightcodmean[:,0],leftcodmean[:,0])
unicod = np.unique(codes[:])

maskright = np.in1d(unicod,rightcodmean[:,0])
maskrightindex = np.searchsorted(rightcodmean[:,0],unicod)



maskleft = np.in1d(unicod,leftcodmean[:,0])
maskleftindex = np.searchsorted(leftcodmean[:,0],unicod)
base_path = "T:\\Darcy\\COMA-PLASTER\\"

camrcolor = cv2.imread(base_path + "CAMR/CAM001.png");
camrcolol = cv2.imread(base_path + "CAML/CAM101.png");



kk = 0
m = unicod.size
print ('Total points on left and right cameras= ',m)
matchpixels = np.zeros([4])
xyz = np.zeros([m,3])
xyzcolor = np.zeros([m,3],dtype=np.uint8)
# finding common points between two cameras and calculating XYZ
for ii in range(0, m-1):
    if (maskleft[ii] and maskright[ii]):
        matchpixels[0] = rightcodmean[maskrightindex[ii],1]
        matchpixels[1] = rightcodmean[maskrightindex[ii],2]
        matchpixels[2] = leftcodmean[maskleftindex[ii],1]
        matchpixels[3] = leftcodmean[maskleftindex[ii],2]
        xyzdata,abdist = camxyzparam([matchpixels[0],matchpixels[1],matchpixels[2],matchpixels[3]])
        #check if the points is in specified limit and distance between rays less than some values
        if ((np.linalg.norm(abdist) < 20) 
            and (xyzdata[2] > 400 and xyzdata[2] < 2000 
             and xyzdata[0] > -500 and xyzdata[0] < 500)):
           xyz[kk,0], xyz[kk,1], xyz[kk,2] = -xyzdata[0], -xyzdata[1], -xyzdata[2]
           # color info from average of image from both cameras
           xyzcolor[kk,0] = (camrcolor[int(matchpixels[1]),int(matchpixels[0]),2]/2+camrcolol[int(matchpixels[3]),int(matchpixels[2]),2]/2)
           xyzcolor[kk,1] = (camrcolor[int(matchpixels[1]),int(matchpixels[0]),1]/2+camrcolol[int(matchpixels[3]),int(matchpixels[2]),1]/2) 
           xyzcolor[kk,2] = (camrcolor[int(matchpixels[1]),int(matchpixels[0]),0]/2+camrcolol[int(matchpixels[3]),int(matchpixels[2]),0]/2)
           kk = kk + 1

print ('Total points = ', kk - 1)








def saveAll(base_path, kk, xyz, xyzcolor):
    # open a PLY file to save the XYZ and colors of point cloud
    ff = open(base_path + "/" + "pointcloud.ply","w")
    ff.write('ply\n')
    ff.write('format ascii 1.0\n')
    ff.write('comment PCL generated\n')
    ff.write('element vertex %d\n'%(kk-1))
    ff.write('property float x\n')
    ff.write('property float y\n')
    ff.write('property float z\n')
    ff.write('property uchar red\n')
    ff.write('property uchar green\n')
    ff.write('property uchar blue\n')
    ff.write('end_header\n')


    xs = open(base_path+"/"+"xs.csv","w")
    ys = open(base_path+"/"+"ys.csv","w")
    zs = open(base_path+"/"+"zs.csv","w")
    for ii in range(0, kk-1):
        ff.write(str(xyz[ii,0])+" "+str(xyz[ii,1])+" "+str(xyz[ii,2])+" "+str(xyzcolor[ii,0])+" "+str(xyzcolor[ii,1])+" "+str(xyzcolor[ii,2])+"\n")       
        xs.write(str(xyz[ii,0]) + "\n")
        ys.write(str(xyz[ii,1]) + "\n")
        zs.write(str(xyz[ii,2]) + "\n")
    ff.close()
    xs.close()
    ys.close()
    zs.close()


#==================================================================
#==================================================================
#==================================================================

XYZ,abdist = camxyzparam([960,540,960,540]) # test function
print (XYZ)









saveAll(base_path, kk, xyz, xyzcolor)
print ('calcxyzcolor Done!\n\n\n')

