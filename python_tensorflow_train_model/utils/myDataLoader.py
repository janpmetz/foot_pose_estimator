import numpy as np

def splitData(data, percentage):
    n = data.shape[0]
    p = percentage / 100.0
    nTrain = int(n * p)
    train = data[0:nTrain, :]
    test = data[nTrain+1 : n, :]
    return train, test

def splitDataTransp(data, percentage):
    n = data.shape[1]
    p = percentage / 100.0
    nTrain = int(n * p)
    train = np.transpose(data[:, 0:nTrain])
    test = np.transpose(data[:, nTrain+1 : n])
    return train, test

def getRandBatch(data, batchSize):
    n = data.shape[0]
    idxs = np.random.randint(0, high=n, size=batchSize)
    return data[idxs, :]

def separateXY(data, clsIdx):
    cols = data.shape[1]
    x = data[:, range(clsIdx)]
    y = data[:, clsIdx:cols]
    return x, y

def split_by_idxs(data, idxs):
    n = len(idxs)
    cols = data.shape[1]
    res = []
    idxs = [0] + idxs
    for i in range(n):
        parti = data[:, idxs[i]:idxs[i+1]]
        res = res + [parti]
    res = res + [data[:, idxs[n]:cols]]
    return res

def onlyCoords(pts):
    # select only the coordinates, leave out the values at the coordinates
    return pts[:, [0,1,3,4,6,7]]
