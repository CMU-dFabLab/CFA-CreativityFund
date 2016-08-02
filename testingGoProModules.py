#based on code from https://gist.github.com/thearn/5562029

import base64
import time
import urllib.request
import cv2
import numpy as np
import os
import inspect

#HINTS:
#to obtain the password http://10.5.5.9/camera/sd
#http://10.5.5.9/camera/PV?t=PASSWORD&p=%02
#http://10.5.5.9:8080/live/amba.m3u8

""" 1 GOPROLIB MODULE """
#import goprolib.HERO4.HERO4 as HERO4 #only for gopro 4
#if __name__ == '__main__':
#    h4 = HERO4.HERO4()
#    print (dir(h4))
#    h4._autoconfigure()
#    h4.watch_status()



""" 2 GOPROMODULE """
#from gopro import GoPro #library files are not updated for python 3!!!



""" 3 GOPROHERO MODULE """
from goprohero import GoProHero 
#works, but some functions are outdated ... it also has 2 complementary modules
#goprocontroller and goprocontrollerui to use multiple cameras!!!!  
camera = GoProHero(password='20abbrobot14')
camera._ip
#test(http://10.5.5.9/camera/sd)
#camera.image()
#image capture is producing the error 
#"warning: Error opening file (/build/opencv/modules/videoio/src/cap_ffmpeg_impl.hpp:578)"
#but I used a test file in python and the ffmpeg codec seems to be ok.

#camera.command('power', 'sleep')
#camera.command('power', 'on')
#camera.command('record', 'on')
#cv2.waitKey(5000)
#camera.command('record', 'off')
#status = camera.status()



"""
4 CAMERA OBJECTS FOR OPENCV (INCLUDING IP CAMERAS)
Examples of objects for image frame aquisition from both IP and
physically connected cameras
Requires:
 - opencv (cv2 bindings)
 - numpy
"""
class ipCamera(object):

    def __init__(self, url, user=None, password=None):
        self.url = url
        auth_encoded = base64.encodestring('%s:%s' % (user, password))[:-1]
        self.req = urllib.request.Request(self.url)
        self.req.add_header('Authorization', 'Basic %s' % auth_encoded)

    def get_frame(self):
        response = urllib.request.urlopen(self.req)
        img_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
        frame = cv2.imdecode(img_array, 1)
        return frame

class Camera(object):

    def __init__(self, camera=0):
        self.cam = cv2.VideoCapture(camera)
        if not self.cam:
            raise Exception("Camera not accessible")

        self.shape = self.get_frame().shape

    def get_frame(self):
        _, frame = self.cam.read()
        return frame

def parsingMjpeg(address):

    """ 
    based on code from 
    http://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera
    """
    #address = 'http://localhost:8080/frame.mjpg'
    stream = urllib.urlopen(address)
    bytes = ''
    while True:
        """
        Mjpeg over http is multipart/x-mixed-replace with boundary frame info and 
        jpeg data is just sent in binary. So you don't really need to care 
        about http protocol headers. All jpeg frames start with marker 0xff 0xd8 
        and end with 0xff 0xd9. So the code above extracts such frames from 
        the http stream and decodes them one by one. like below.
        """
        bytes += stream.read(1024) #this is incrementally slicing the file
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = bytes[a:b+2]
            bytes= bytes[b+2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
            cv2.imshow('i',i)
            if cv2.waitKey(1) == 27:
                exit(0)   