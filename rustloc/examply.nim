import nimpy
import scinim/numpyarrays
import scinim
import std/[sequtils]

proc doStuff[T: SomeFloat](el: T) : T {.inline.} =
  result = (1.0-el)/(1.0+el)

proc modArray*(x: NumpyArray[float64]) {.exportpy.} =
  # echo "modArrayInPlace.nim"
  # Example of accessing the buffer directly
  x[0, 0] = 123.0
  x[0, 1] = -5.0

proc parallelForOp*(x: NumpyArray[float64]) {.exportpy.} =
  let
    ux = x.toUnsafeView()
  for i in 0||(x.len-1):
    ux[i] = doStuff ux[i]

proc parallelIndexedForOp*(x: NumpyArray[float64])  {.exportpy.} =
  fuseLoops("parallel for"):
    for i in 0..<x.shape[0]:
      for j in 0..<x.shape[1]:
        x[i, j] = doStuff x[i, j]

proc normalForOp*(x: NumpyArray[float64]) {.exportpy.} =
  for i in 0..(x.len-1):
    x{i} = doStuff x{i}

proc indexedOp*(x: NumpyArray[float64]) {.exportpy.} =
  for i in 0..<(x.shape[0]):
    for j in 0..<(x.shape[1]):
      x[i, j] = doStuff x[i, j]

proc runCalc*(x: NumpyArray[float64]) : float64 {.exportpy.} =
  result = 0.0
  for i in 0..<x.len:
    result += doStuff x{i}
