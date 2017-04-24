import sys
import os

def myMakeDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def setElemsOne(array, elemsIdx):
    # array of eg. 1000, 10, 10 and set within the 10,10 array the elements 1 that are specified in elems idx of e.g size 1000, 2
    for i in range(elemsIdx.shape[0] - 1):
        array[i, elemsIdx[i, 0].astype(int), elemsIdx[i, 1].astype(int)] = 1


def setElems(array, elemsIdx, x):
    # array of eg. 1000, 10, 10 and set within the 10,10 array the elements 1 that are specified in elems idx of e.g size 1000, 2
    for i in range(elemsIdx.shape[0]):
        array[i, elemsIdx[i, 0].astype(int), elemsIdx[i, 1].astype(int)] = x

def setElems2d(array, elemsIdx, x, dataWidth):
    # ASSUMPTION_ start counting with 0s
    cols = array.shape[1]
    for i in range(elemsIdx.shape[0]):
        idx = ((elemsIdx[i, 0].astype(int)) * dataWidth) + elemsIdx[i, 1].astype(int)
        array[i, idx] = x