import zmq
import cv2
import base64


# source image using imread
def converttobase64(img):
    print "test"
    # cnt = cv2.imwrite("kenteken.png", img)
    cnt = cv2.imencode('.png',img)[1]
    return base64.encodestring(cnt)


context = zmq.Context()
socket = context.socket(zmq.REP)
connectionString = "127.0.0.1:9023"

socket.bind("tcp://" + connectionString)
print "Server started on %s" % connectionString
print "waiting for client connection"

#first wait for hello message
message = socket.recv()
print "message received: %s" % message
# socket.send_string(message)


print "send image test"
# source image
img = cv2.imread('img/kenteken-apart.png')
b64 = converttobase64(img)
print b64
socket.send_string(b64)


def debug():
    while True:
        # Wait for next request from client
        message = socket.recv()
        print "message received: %s" % message
        socket.send_string(message)




def waitforanswer():
    while True:
        #  Wait for next request from client
        message = socket.recv()
        return message

# # Define a function for the thread
# def print_time(threadName, delay):
#     count = 0
#     while count < 5:
#         time.sleep(delay)
#         count += 1
#         print "%s: %s" % (threadName, time.ctime(time.time()))
#
#
# # Create two threads as follows
# try:
#     thread.start_new_thread(server, ())
# except:
#     print "Error: unable to start thread"
#
# while 1:
#     pass
