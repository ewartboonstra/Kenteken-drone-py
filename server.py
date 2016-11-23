import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
connectionString = "145.44.81.71:9023"

socket.bind("tcp://" + connectionString)
print "Server started on %s" % connectionString

while True:
    #  Wait for next request from client
    message = socket.recv()
    print "message received: %s" % message
    socket.send_string(message)


def sentImage():
    print "test"


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
