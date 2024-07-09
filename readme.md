# Deps

System  :zmq (brew install zmq)
Python : python-3.11, pyzmq (simulate a MQ)
Nim : nim-taskpools (audited thread pool), nim-zmq (high-level bindings of libzmq), nimpy (high-level binding of Python3)

## Installation

```
brew install python3.11
brew install zmq
python3.11 -m pip install zmq
brew install nim
```

Then setup the workspace:
```
git clone $(THIS_PROJECT)
cd $(THIS_PROJECT)
atlas rep 
cd pynimlocal/
./run.sh
```
