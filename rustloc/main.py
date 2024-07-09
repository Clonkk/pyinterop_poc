#!python3
import examply_rs as rs
import examply as nm

import numpy as np
from timeit import default_timer as timer
import multiprocessing

def fLoop(ar):
    s = 0.0
    iX = int(ar.shape[0])
    iY = int(ar.shape[1])

    for i in range(0, iX):
        for j in range(0, iY):
            el = ar[i, j]
            s = s + (1-el)/(1+el)
    print("res=", s)
    return s

def runCalc(ar, timePythonLoop=False):
    print(ar)
    print("1)")
    # Toggle - CAREFUL it takes a long time since Python is slow
    if timePythonLoop:
        start = timer()
        pyres = fLoop(ar)
        end = timer()
        print("Python loop took : ", end-start, " seconds")
        print("pyres=", pyres)

    start = timer()
    res = rs.runCalc(ar)
    end = timer()
    print("Python measured Rust loop took : ", end-start, " seconds")

    start = timer()
    res2 = nm.runCalc(ar)
    end = timer()
    print("Python measured Nim loop took : ", end-start, " seconds")

    status = np.isclose(res, res2)
    if timePythonLoop:
        status = np.isclose(res, res2) and np.isclose(res, pyres)
    print(f"Test result identical: {status}")


def modArray(ar):
    print("2) Showing in-place mod")
    print(ar[0, 0:3])
    rs.modArray(ar)
    nm.modArray(ar)
    print(ar[0, 0:3])


def compareLoops(ar, rustfn, nimfn):
    start = timer()
    arr0 = np.copy(ar)
    rustfn(arr0)
    end = timer()
    print(f"Rust => {rustfn.__name__}: ", end-start, " seconds")

    start = timer()
    arr1 = np.copy(ar)
    nimfn(arr1)
    end = timer()
    print(f"Nim  => {nimfn.__name__}: ", end-start, " seconds")

    eq = np.allclose(arr0, arr1)
    eq2 = np.max(arr0 - arr1)
    print("----------------")
    print(f"{nimfn.__name__} ==  {rustfn.__name__} = {eq}. Max diff: {eq2}")
    result = arr1
    print("")
    return result


def forLoops(ar, timePythonLoop=False):
    print("3) Comparing for loops")
    arr0 = compareLoops(ar, rs.normalForOp, nm.normalForOp)
    arr1 = compareLoops(ar, rs.indexedOp, nm.indexedOp)
    arr3 = compareLoops(ar, rs.parallelForOp, nm.parallelForOp)
    arr4 = compareLoops(ar, rs.parallelIndexedForOp, nm.parallelIndexedForOp)

    if timePythonLoop:
        start = timer()
        arr2 = np.zeros(ar.shape)
        X = int(ar.shape[0])
        Y = int(ar.shape[1])
        for i in range(0, X):
            for j in range(0, Y):
                arr2[i, j] = (1.0-ar[i, j])/(1.0+ar[i, j])
        end = timer()
        print("Native python for: ", end-start, " seconds")

    # We can check that it returns a copy
    # print(np.shares_memory(ar, arr0))
    # print(np.shares_memory(ar, arr1))

    # Check results are identical
    eq = np.allclose(arr0, arr1)
    eq = eq and np.allclose(arr0, arr3)
    eq = eq and np.allclose(arr0, arr4)
    if timePythonLoop:
        eq = eq and np.allclose(arr0, arr2)

    print(f"Global tests results:{eq}")
    print("----------------")
    print("END")

def main():
    print("Python => main()")
    MAX_X = int(2*1e4)
    MAX_Y = int(6*1e4)
    MAX_LEN = int(MAX_X*MAX_Y)
    print("CPU COUNT=",  multiprocessing.cpu_count())
    print("MAX_X=", MAX_X)
    print("MAX_Y=", MAX_Y)
    print("MAX_LEN=", MAX_LEN)
    ar = np.random.rand(MAX_X, MAX_Y)
    timePythonLoop = False
    print("BEGIN")
    print("----------------")
    runCalc(ar, timePythonLoop)
    modArray(ar)
    forLoops(ar, timePythonLoop)


main()
## In bash, simply run :
## time nim c examply && time python3 examply.py > results.txt
## This takes about ~30 minutes due to long python loop

