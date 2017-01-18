import base64

from Photo import Photo
from jsondata import Json
from plate_finder import plate_finder
import server
import cv2

if __name__ == '__main__':
    plate_finder = plate_finder()
    foto = Photo()
    go = True
    while go:
        try:
            img = foto.takePhoto()
        except:
            print "no conection"
            img = cv2.imread('img/stupidtest.JPG', cv2.IMREAD_COLOR)

        '''from glob import glob
        for fn in glob('img/*.JPG'):'''

        #img = cv2.imread(fn, cv2.IMREAD_COLOR)
        cords = plate_finder.find_squares(img)
        #for debugging purposes to c the imiage during run time
        '''cv2.namedWindow('full img', cv2.WINDOW_NORMAL)
        cv2.imshow('full img', img)
        ch = 0xFF & cv2.waitKey()'''

        for cord in cords:
            print cord
            bounding  = cv2.boundingRect(cord)
            print bounding
            crop_img = img[bounding[1]:bounding[1]+bounding[3], bounding[0]:bounding[0]+bounding[2]]  # Crop from x, y, w, h -> 100, 200, 300, 400
            # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]

            #for debugging purposes to c the imiage during run time
            #cv2.namedWindow('crop', cv2.WINDOW_NORMAL)
            #cv2.imshow('crop', crop_img)

            cv2.imwrite("tmp_crop.png", crop_img)

            cropped_img = cv2.imread("tmp_crop.png", cv2.IMREAD_COLOR)
            #send image to server
            # test code
            #jsonData = base64.b64encode(cropped_img)
            # echte code
            json = Json()
            jsonData = json.convertToJson(cropped_img)

            server = server.Server()
            server.openConnection()
            server.sendJsonData(jsonData)
            server.closeConnection()

            '''ch = 0xFF & cv2.waitKey()
            if ch == 27:
                break
            cv2.destroyAllWindows()'''
            #print cords
        '''ch = 0xFF & cv2.waitKey()
        if ch == 27:
            go = False
        cv2.destroyAllWindows()'''
