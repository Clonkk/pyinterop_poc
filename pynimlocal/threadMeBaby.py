import sys

USE_PY_VERSION = 0

if len(sys.argv) > 1 and str(sys.argv[1]) == "py":
    USE_PY_VERSION = 1

if USE_PY_VERSION:
    import pythonfunc as func
else:
    import nativefunc as func

import zmq

import random
import time

MAX_MSG_SENT = 100 

def bind(port):
    # Send a 100 message on a messaging queue
    # Some 'topic' will act as worker from native code in a threaded way
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    msgsent = 0
    while msgsent < MAX_MSG_SENT:
        topic = random.randrange(9999,10005)
        messagedata = random.randrange(1,215) - 80
        print("%d %d" % (topic, messagedata))
        socket.send_string("%d %d" % (topic, messagedata))
        msgsent = msgsent + 1
        time.sleep(0.1)


def main():
    print("Py => main")
    port = "33333"
    t1 = "10001"
    t2 = "10002"
    t3 = "10003"
    func.connect(port, t1)
    func.connect(port, t2)
    func.connect(port, t3)
    time.sleep(1)
    print("bind()")
    bind(port)
    res = func.aggregate_result()
    print(res)

main()
