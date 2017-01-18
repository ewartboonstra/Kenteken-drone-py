import urllib2
import json
import time
import cv2
import numpy as np


class Photo:
    class __Photo:
        def __init__(self):
            pass

    instance = None

    def __init__(self):
        if not Photo.instance:
            Photo.instance = Photo.__Photo()
        else:
            print "class already exists"

    def shootPhoto(self):
        photoUrl = "http://10.5.5.9/gp/gpControl/command/shutter?p=1"
        print "Waiting for wifi connection."
        urllib2.urlopen(photoUrl)
        print "photo taken"
        time.sleep(1.5)  # 1.5 second interval to make sure photo saves

    def getPhotoUrl(self):
        # save photo
        url = "http://10.5.5.9/gp/gpMediaList/"
        response = urllib2.urlopen(url)
        data = json.loads(response.read())
        response.close()
        length = len(data['media'][0]['fs'])
        name = data['media'][0]['fs'][length - 1]['n']
        print "photo name: " + name
        return "http://10.5.5.9:8080/videos/DCIM/100GOPRO/" + name

        # download the image, convert it to a NumPy array, and then read

    # METHOD #1: OpenCV, NumPy, and urllib

    def url_to_image(self, url):
        # it into OpenCV format
        resp = urllib2.urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        # return the image
        return image


        # Maakt foto en returnt een cv2 image
        # Hiervoor moet je verbonden zijn met de gopro wifinetwerk
    def takePhoto(self):
        photo = Photo()
        photo.shootPhoto()
        path = photo.getPhotoUrl()
        print "Image made"
        return photo.url_to_image(path)
