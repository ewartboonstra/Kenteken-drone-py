import zmq
import cv2
import base64


class Server:
    class __Server:
        def __init__(self):
            pass

    instance = None

    def __init__(self):
        if not Server.instance:
            Server.instance = Server.__Server()
        else:
            print "class already exists"

    # initiate server functions
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)

    # Convert to base64 image for easy transferring
    def convertToBase64(self, img):
        cnt = cv2.imencode('.png', img)[1]
        return base64.encodestring(cnt)

    # open connection to c# server
    def openConnection(self):
        connectionString = "127.0.0.1:9023"

        self.socket.bind("tcp://" + connectionString)
        print "Connected to server on %s" % connectionString

    # Close server connection
    def closeConnection(self):
        self.socket.close()
        print "Connection closed"

    # Send image of kenteken to c# server
    def sendImg(self, img):
        # debug image
        # img = cv2.imread('img/kenteken-apart.png')
        b64 = self.convertToBase64(img)
        self.socket.send_string(b64)
        print "Image sent"
