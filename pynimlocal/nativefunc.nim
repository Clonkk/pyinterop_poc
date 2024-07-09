import
  nimpy,
  taskpools,
  zmq,
  std/[times, monotimes, os, strformat, strutils]

const nthreads = 4
var tp = Taskpool.new(num_threads = nthreads)
var results : seq[FlowVar[int]]

proc connectImpl(port, topic: string) : int =
  var con = connect(fmt"tcp://localhost:{port}", SUB)
  sleep(1000)
  discard con.setsockopt(SUBSCRIBE, topic)
  echo "fromNim: SUBSCRIBE OK"
  var total_value = 0
  for i in 0..<5:
    let s = con.receive()
    echo fmt"thread[{topic} fromNim: {s}"
    var msgdata = s.split()[1]
    total_value += parseInt(msgdata)

  echo fmt"total msgdata value for topic {topic} was {total_value}"
  con.close()
  total_value

proc connect*(port: Pyobject, topic: PyObject) {.exportpy.}=
  echo "runInThread called"
  let port = port.to(string)
  let topic = topic.to(string)
  results.add tp.spawn connectImpl(port, topic)

proc aggregate_result*() : seq[int] {.exportpy.} =
  for r in results:
    result.add r.sync()

  tp.syncAll()
  tp.shutdown()
