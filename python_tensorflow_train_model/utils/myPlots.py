import matplotlib.pyplot as plt
from random import randint
import numpy as np

def plotShapes(x, yReal, yPred, zmp, nonBlocking):
    #colorSheme='nipy_spectral'
    colorSheme='jet'

    fig = plt.figure(1)
    fig.suptitle('CONTACT POINTS')

    n = 5
    rows = x.shape[0]
    randRange = [randint(0, rows-1) for p in range(0, n)]

    pltCount = 0
    for i in randRange:
        idx = pltCount*3
        plt.subplot(n, 3, idx+1)
        plt.title('terrain')
        plt.axis('off')
        plt.imshow(np.reshape(x[i,:], (10, 10)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        plt.plot(zmp[1], zmp[0], 'rx')

        plt.subplot(n, 3, idx+2)
        plt.title('ground truth')
        plt.axis('off')
        plt.imshow(np.reshape(yReal[i,:], (10, 10)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        plt.plot(zmp[1], zmp[0], 'rx')

        plt.subplot(n, 3, idx+3)
        plt.title('prediction')
        plt.axis('off')
        plt.imshow(np.reshape(yPred[i,:], (10, 10)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        plt.plot(zmp[1], zmp[0], 'rx')
        pltCount = pltCount+1
    if(nonBlocking):
        plt.draw()
        plt.pause(0.001)
    else:
        plt.show()

# always plot what you are dealing with
#plotShapes(train_x, train_edgePts, train_ctPts, train_zmp)
#plotShapes(train_x, train_zmp_array, train_zmp_array, train_zmp)
#plotShapes(test_x, test_zmp_array, test_zmp_array, test_zmp)
