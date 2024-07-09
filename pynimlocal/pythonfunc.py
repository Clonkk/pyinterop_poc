import zmq
import threading

global_results = []
thrs = []

# Mock-up of a client received data from a messaging queue and doing some work
# Results needs to be aggregated with other worker
def connectImpl(port: str, topicfilter: str) -> int:
    # Socket to talk to server
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect ("tcp://localhost:%s" % port)
    socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
    # Process 5 updates
    total_value = 0
    for i in range (5):
        string = socket.recv_string()
        topic, messagedata = string.split()
        total_value += int(messagedata)
        print(topic, messagedata)

    print("Total messagedata value for topic '%s' was %dF" % (topicfilter, total_value))
    global_results.append(total_value)

def connect(port: str, topicfilter: str) -> int:
    thr1 = threading.Thread(target=connectImpl, args=(port, topicfilter,))
    thr1.start()
    thrs.append(thr1)

def aggregate_result() -> list[int]:
    for thr in thrs:
        thr.join()
    return global_results

