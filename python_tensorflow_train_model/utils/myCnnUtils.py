import matplotlib.pyplot as plt
from random import randint
import numpy as np
import time
import myUtils

def plotShapes(x, yReal, yPred, zmp):
    #colorSheme='nipy_spectral'
    colorSheme='jet'

    fig = plt.figure()
    fig.suptitle('CONTACT POINTS')

    n = 5
    rows = x.shape[0]
    randRange = [randint(0, rows-1) for p in range(0, n)]
    #randRange = [1,2,3,4,5]

    pltCount = 0
    for i in randRange:
        idx = pltCount*3
        plt.subplot(n, 3, idx+1)
        plt.title('terrain')
        plt.axis('off')
        plt.imshow(np.reshape(x[i,:], (20, 20)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        plt.plot(zmp[i,1], zmp[i,0], 'rx')


        plt.subplot(n, 3, idx+2)
        plt.title('ground truth')
        plt.axis('off')
        plt.imshow(np.reshape(yReal[i,:], (20, 20)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        plt.plot(zmp[i,1], zmp[i,0], 'rx')


        plt.subplot(n, 3, idx+3)
        plt.title('prediction')
        plt.axis('off')
        plt.imshow(np.reshape(yPred[i,:], (20, 20)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        plt.plot(zmp[i,1], zmp[i,0], 'rx')

        pltCount = pltCount+1
    plt.show()

def plotShapes_2(x, yReal, yPred, dataWidth, dataHeight, plotPath):
    colorSheme='nipy_spectral'
    #colorSheme = 'jet'

    fig = plt.figure(1)
    fig.suptitle('CONTACT POINTS')

    n = 5
    rows = x.shape[0]
    #randRange = [randint(0, rows - 1) for p in range(0, n)]
    randRange = [1,2,3,4,5]

    pltCount = 0
    for i in randRange:
        idx = pltCount * 3
        plt.subplot(n, 3, idx + 1)
        plt.title('terrain')
        plt.axis('off')
        plt.imshow(np.reshape(x[i, :], (dataWidth, dataHeight)), cmap=plt.get_cmap(colorSheme)) # todo is width and height or height and with?
        plt.hold(True)
        #plt.plot(zmp[i, 1], zmp[i, 0], 'rx')

        plt.subplot(n, 3, idx + 2)
        plt.title('ground truth')
        plt.axis('off')
        plt.imshow(np.reshape(yReal[i, :], (dataWidth, dataHeight)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        #plt.plot(zmp[i, 1], zmp[i, 0], 'rx')

        plt.subplot(n, 3, idx + 3)
        plt.title('prediction')
        plt.axis('off')
        plt.imshow(np.reshape(yPred[i, :], (dataWidth, dataHeight)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        #plt.plot(zmp[i, 1], zmp[i, 0], 'rx')

        pltCount = pltCount + 1
    #plt.show(block=False)
    #plt.show()
    #plt.draw()
    plt.pause(0.1)
    #plt.clf()
    plt.savefig(plotPath)



def plotShapes_2_andZMP(x, yReal, yPred, dataWidth, dataHeight, plotPath, zmp):
    #colorSheme='nipy_spectral'
    colorSheme = 'jet'

    yReal = yReal *255
    #yPred = yPred *255

    fig = plt.figure(1)
    fig.suptitle('CONTACT POINTS')

    n = 5
    rows = x.shape[0]
    randRange = [randint(0, rows - 1) for p in range(0, n)]
    #randRange = [0,1,2,3,4]

    pltCount = 0
    for i in randRange:

        #yReal[i,zmp[i,0]] = 50

        idx = pltCount * 3
        plt.subplot(n, 3, idx + 1)
        plt.title('terrain')
        plt.axis('off')
        plt.imshow(np.reshape(x[i, :], (dataWidth, dataHeight)), cmap=plt.get_cmap(colorSheme)) # todo is width and height or height and with?
        plt.hold(True)
        #plt.plot(zmp[i, 1], zmp[i, 0], 'rx')

        plt.subplot(n, 3, idx + 2)
        plt.title('ground truth')
        plt.axis('off')
        plt.imshow(np.reshape(yReal[i, :], (dataWidth, dataHeight)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        #plt.plot(zmp[i, 1], zmp[i, 0], 'rx')

        plt.subplot(n, 3, idx + 3)
        plt.title('prediction')
        plt.axis('off')
        plt.imshow(np.reshape(yPred[i, :], (dataWidth, dataHeight)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        #plt.plot(zmp[i, 1], zmp[i, 0], 'rx')

        pltCount = pltCount + 1
    #plt.show(block=False)
    plt.show()
    #plt.draw()
    #plt.pause(0.1)
    #plt.clf()
    plt.savefig(plotPath)






def plotShapes_2_first(x, yReal, yPred, dataWidth, dataHeight, plotPath):
    colorSheme='nipy_spectral'
    #colorSheme = 'jet'

    fig = plt.figure(1)
    fig.suptitle('CONTACT POINTS')

    n = 5
    rows = x.shape[0]
    #randRange = [randint(0, rows - 1) for p in range(0, n)]
    randRange = [1,2,3,4,5]

    pltCount = 0
    for i in randRange:
        idx = pltCount * 3
        plt.subplot(n, 3, idx + 1)
        plt.title('terrain')
        plt.axis('off')
        plt.imshow(np.reshape(x[i, :], (dataWidth, dataHeight)), cmap=plt.get_cmap(colorSheme)) # todo is width and height or height and with?
        plt.hold(True)
        #plt.plot(zmp[i, 1], zmp[i, 0], 'rx')

        plt.subplot(n, 3, idx + 2)
        plt.title('ground truth')
        plt.axis('off')
        plt.imshow(np.reshape(yReal[i, :], (dataWidth, dataHeight)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        #plt.plot(zmp[i, 1], zmp[i, 0], 'rx')

        plt.subplot(n, 3, idx + 3)
        plt.title('prediction')
        plt.axis('off')
        plt.imshow(np.reshape(yPred[i, :], (dataWidth, dataHeight)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        #plt.plot(zmp[i, 1], zmp[i, 0], 'rx')

        pltCount = pltCount + 1
    #plt.show(block=False)
    #plt.show()
    #plt.draw()
    plt.pause(0.1)
    #plt.clf()
    plt.savefig(plotPath)





def plotShapes_pts(x, yReal, yPred, dataWidth, dataHeight): #terrain_test, cps_test, preds, dataWidth, dataHeight
    # colorSheme='nipy_spectral'
    colorSheme = 'jet'

    #fig = plt.figure(1)
    #fig.suptitle('CONTACT POINTS')

    n = 3
    rows = x.shape[0]
    #randRange = [randint(0, rows - 1) for p in range(0, n)]
    randRange = [0, 1, 2]

    # scale up again (just temporary)
    yReal = yReal * 100
    yPred = yPred * 100

    x_real_idx = np.round(yReal / dataWidth)           # todo is width and height or height and with?
    y_real_idx = np.mod(yReal, dataHeight)

    x_pred_idx = np.round(yPred / dataWidth)           # todo is width and height or height and with?
    y_pred_idx = np.mod(yPred, dataHeight)


    '''
    THE PERMUTATIONS !!!!!!!!!!!!!
    '''

    # todo other_plots are wrongg

    pltCount = 0
    for i in randRange:
        idx = pltCount * 3
        plt.subplot(n, 3, idx + 1, axisbg='white')
        plt.title('terrain')
        #plt.axis('off')
        plt.imshow(np.reshape(x[i, :], (dataWidth, dataHeight)), cmap=plt.get_cmap(colorSheme)) # todo is width and height or height and with?
        plt.hold(True)
        #plt.plot(zmp[i, 1], zmp[i, 0], 'rx')

        plt.subplot(n, 3, idx + 2, axisbg='white')
        plt.title('ground truth')
        #plt.axis('off')
        plt.scatter(x_real_idx[i,:], y_real_idx[i,:])
        plt.hold(True)
        #plt.plot(zmp[i, 1], zmp[i, 0], 'rx')

        plt.subplot(n, 3, idx + 3, axisbg='white')
        plt.title('prediction')
        #plt.axis('off')
        plt.scatter(x_pred_idx[i,:], y_pred_idx[i,:])
        plt.hold(True)
        #plt.plot(zmp[i, 1], zmp[i, 0], 'rx')


        pltCount = pltCount + 1
    #plt.show(block=False)
    #plt.show()
    #plt.draw()
    plt.pause(0.1)
    plt.clf()
