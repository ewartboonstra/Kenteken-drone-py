import zmq
import cv2
import base64


# Convert to base64 image for easy transferring
def convertToBase64(img):
    cnt = cv2.imencode('.png', img)[1]
    return base64.encodestring(cnt)


# open connection to c# server
def OpenConnection():
    connectionString = "127.0.0.1:9023"

    socket.bind("tcp://" + connectionString)
    print "Connected to server on %s" % connectionString


# Close server connection
def closeConnection():
    socket.close()
    print "Connection closed"


# Send image of kenteken to c# server
def sendImg(img):
    # debug image
    # img = cv2.imread('img/kenteken-apart.png')
    b64 = convertToBase64(img)
    socket.send_string(b64)
    print "Image sent"


context = zmq.Context()
socket = context.socket(zmq.PAIR)
