#!/usr/bin/env python
import os
import scipy.io
import sys
import time
from random import randint

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from final import myUtils

from utils import myDataLoader as myLoader

############################################# CONFIG

fileName = '../training_data/data_edgePts_50k.mat'
matName = 'training_data'
clsIdx = 100  # counting from 0
trainTestSplit = 66
dataWidth = 10
dataHeight = 10
dataLen = dataWidth*dataHeight
batchSize = 50
nRuns = 5000
script_name = os.path.basename(sys.argv[0]).replace(".py", "")

def myMakeDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

timeStr = time.strftime('%m_%d_%H_%M')  # easy to sort by filename
path = "models/mycnn_arch_"+script_name
myMakeDir(path)
path = path +"/model_mycnn_"+timeStr+".ckpt"
logPath = "logs/mycnn_arch_"+script_name+"/logs_mycnn_"+timeStr
myMakeDir(logPath)

############################################# LOAD DATA
# todo: first form then split
mat = scipy.io.loadmat(fileName)
data = mat[matName]

train, test = myLoader.splitData(data, trainTestSplit)

clsIdx1 = 100
clsIdx2 = 200
clsIdx3 = 300
train_terrain, train_edgePts, train_ctPts, train_zmp = myLoader.my4SplitData(train, clsIdx1, clsIdx2, clsIdx3)
test_terrain, test_edgePts, test_ctPts, test_zmp = myLoader.my4SplitData(test, clsIdx1, clsIdx2, clsIdx3)

# reshape to "images"
#train_terrain = train_terrain.reshape(-1, 10, 10, 1)
#test_terrain = test_terrain.reshape(-1, 10, 10, 1)
#train_edgePts = train_edgePts.reshape(-1, 10, 10)
#test_edgePts = test_edgePts.reshape(-1, 10, 10)
#train_ctPts = train_ctPts.reshape(-1, 10, 10, 1)
#test_ctPts = test_ctPts.reshape(-1, 10, 10, 1)

train_terrain = train_terrain.reshape(-1, 100)
test_terrain = test_terrain.reshape(-1, 100)
train_edgePts = train_edgePts.reshape(-1, 100)
test_edgePts = test_edgePts.reshape(-1, 100)
train_ctPts = train_ctPts.reshape(-1, 100)
test_ctPts = test_ctPts.reshape(-1, 100)


train_ctPts_ones = np.copy(train_ctPts)
test_ctPts_ones = np.copy(test_ctPts)
train_ctPts_ones[train_ctPts_ones>0]=1
test_ctPts_ones[test_ctPts_ones>0]=1

train_edgePts_ones = np.copy(train_edgePts)
test_edgePts_ones = np.copy(test_edgePts)
train_edgePts_ones[train_edgePts_ones>0]=1
test_edgePts_ones[test_edgePts_ones>0]=1

# model zmp as a input image
train_zmp = train_zmp -1  # matlab starts counting by 1
test_zmp = test_zmp -1
train_zmp_array = np.zeros((train_zmp.shape[0], 10,10))
test_zmp_array = np.zeros((test_zmp.shape[0], 10,10))
myUtils.setElemsOne(train_zmp_array, train_zmp)
myUtils.setElemsOne(test_zmp_array, test_zmp)
train_zmp_array = train_zmp_array.reshape(-1, 100)
test_zmp_array = test_zmp_array.reshape(-1, 100)

# The two channel input (like a picture with r,g,b but now terrain and zmp layers)
'''
X_train = np.zeros((train_zmp.shape[0], 10, 10, 2))
X_train[:,:,:,0] = train_terrain[:,:,:,0]
X_train[:,:,:,1] = train_zmp_array[:,:,:,0]
X_test = np.zeros((test_zmp.shape[0], 10, 10, 2))
X_test[:,:,:,0] = test_terrain[:,:,:,0]
X_test[:,:,:,1] = test_zmp_array[:,:,:,0]
'''

# put all above 1
train_x = train_terrain
test_x = test_terrain
#train_edgePts = train_edgePts
#test_edgePts = test_edgePts
#train_ctPts = train_ctPts*10 +1
#test_ctPts = test_ctPts*10 +1

############################################# HELPER FUNCTIONS
# todo: auslagern
def plotShapes(x, yReal, yPred, zmp):
    #colorSheme='nipy_spectral'
    colorSheme='jet'

    fig = plt.figure()
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
        plt.plot(zmp[i,1], zmp[i,0], 'rx')

        plt.subplot(n, 3, idx+2)
        plt.title('ground truth')
        plt.axis('off')
        plt.imshow(np.reshape(yReal[i,:], (10, 10)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        plt.plot(zmp[i,1], zmp[i,0], 'rx')

        plt.subplot(n, 3, idx+3)
        plt.title('prediction')
        plt.axis('off')
        plt.imshow(np.reshape(yPred[i,:], (10, 10)), cmap=plt.get_cmap(colorSheme))
        plt.hold(True)
        plt.plot(zmp[i,1], zmp[i,0], 'rx')
        pltCount = pltCount+1
    plt.show()

# always plot what you are dealing with
#plotShapes(train_x, train_edgePts, train_ctPts, train_zmp)
#plotShapes(train_x, train_zmp_array, train_zmp_array, train_zmp)
#plotShapes(test_x, test_zmp_array, test_zmp_array, test_zmp)

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

############################################# DEFINE COMPUTATION GRAPH

# Input Tensor with two channels: Terrain and ZMP
# [bathSizeUnspecified, height, width, channels(e.g. rgb)]
#X = tf.placeholder("float", [None, 10, 10, 2])

# Ground truth contact pts
#Y_true_edge = tf.placeholder("float", [None, 100])
#Y_ones_edgePts = tf.placeholder("float", [None, 100])

# Input X
# [bathSizeUnspecified, height, width, channels(e.g. rgb)]
X = tf.placeholder("float", [None, 100])

# Ground truth place holder
YReal_edgePts = tf.placeholder("float", [None, 100])

# densely connected layer
featVec = tf.reshape(X, [-1, 100])
W_dense1 = weight_variable([10 * 10, 10 * 10])
featMap4 = tf.matmul(featVec, W_dense1)
featMap4 = tf.nn.relu(featMap4)
# densely connected layer
W_dense2 = weight_variable([10 * 10, 10 * 10])
featMap5 = tf.matmul(featMap4, W_dense2)
featMap5 = tf.nn.relu(featMap5)
# densely connected layer
W_dense3 = weight_variable([10 * 10, 10 * 10])
featMap6 = tf.matmul(featMap5, W_dense3)
featMap6 = tf.nn.relu(featMap6)
# densely connected layer
W_dense4 = weight_variable([10 * 10, 10 * 10])
featMap7 = tf.matmul(featMap6, W_dense4)
featMap7 = tf.nn.relu(featMap7)

YPred_edgePts = featMap7

########## Contact points:

#EdgePtsAndZMP = tf.placeholder("float", [None, 10 * 10, 2])

ZMP = tf.placeholder("float", [None, 100])
#EdgePtsAndZMP = tf.concat(1, [YPred_edgePts, ZMP])
EdgePtsAndZMP = tf.concat(1, [YReal_edgePts, X])


# Ground truth contact pts
YReal_ctPts = tf.placeholder("float", [None, 100])

W_dense5 = weight_variable([10 * 10 * 2, 10 * 10])
#B1 = bias_variable([10 * 10])
featMap8 = tf.matmul(EdgePtsAndZMP, W_dense5) #+ B1
featMap8 = tf.nn.sigmoid(featMap8)

featMap8 = tf.concat(1, [featMap8, ZMP])
W_dense6 = weight_variable([10 * 10 * 2, 10 * 10 * 2])
#B2 = bias_variable([10 * 10])
featMap9 = tf.matmul(featMap8, W_dense6) #+ B2
featMap9 = tf.nn.sigmoid(featMap9)

W_dense7 = weight_variable([10 * 10  *2, 10 * 10 * 2])
#B3 = bias_variable([10 * 10])
featMap10 = tf.matmul(featMap9, W_dense7) #+ B3
featMap10 = tf.nn.sigmoid(featMap10)

W_dense8 = weight_variable([10 * 10 * 2, 10 * 10])
#B4 = bias_variable([10 * 10])
featMap11 = tf.matmul(featMap10, W_dense8) #+ B4
featMap11 = tf.nn.sigmoid(featMap11)

YPred_ctPts = featMap11

#W_dense5, W_dense6, W_dense7, W_dense8


################################### COMMENTS

'''
bs 64 faster convergence than 128 (lr 0.001)
down to about 5000, 6000

bs 32 & learning_rate=0.0001 drops nice steadily
down to about 5000
nearly perfect results




with added X and ZMP concats and sigmoids:
episodes2 = 5000
bs = 300
lr = 0.0001
(3927, 31836.336, 6652.3384)
(3928, 31836.35, 6652.353)
then it overfits and increases again
'''

############################################# COST FUNCTION and OPTIMIZER

#with tf.name_scope('costContactPts'):
    #cost_ctPts = tf.reduce_sum(tf.pow(Y_true_edge - Y_pred_edge, 2))  # minimize squared error
    #cost_ctPts = tf.reduce_sum(tf.pow(Y_ - Y_pred, 2))*10 + 7*tf.reduce_sum(tf.pow((Y_pred - tf.mul(Y_pred, Y_ones)), 2))
    #cost_ctPts = tf.reduce_sum(tf.pow((Y_ - tf.mul(Y_pred, Y_ones)), 2))*4 + 10*tf.reduce_sum(tf.pow((Y_pred - tf.mul(Y_pred, Y_ones)), 2))
    #cost_ctPts = tf.reduce_sum(tf.pow(Y_ - Y_pred, 2)) + 0.5*tf.reduce_sum(tf.abs((Y_pred - tf.mul(Y_pred, Y_ones))))
    #cost_ctPts = tf.reduce_mean(-tf.reduce_sum(Y_ * tf.log(Y_pred), reduction_indices=[1]))
    #cost_ctPts = tf.reduce_sum(tf.pow(Y_ - Y_pred, 2))*10 + tf.reduce_sum(tf.pow((Y_ - tf.mul(Y_pred, Y_ones)), 2))
    #cost_ctPts = tf.reduce_sum(tf.pow(Y_ - tf.mul(Y_pred, Y_ones),2) + tf.pow((Y_pred - tf.mul(Y_pred, Y_ones)), 2)) # maybe add tf.pow(Y_ - Y_pred, 2))
    #cost_ctPts = tf.reduce_sum(tf.pow(Y_ - Y_pred, 2)*0.2 + tf.pow(Y_ - tf.mul(Y_pred, Y_ones),2) + tf.pow((Y_pred - tf.mul(Y_pred, Y_ones)), 2))
    #cost_ctPts = tf.reduce_sum(tf.pow(Y_true_edge - tf.mul(Y_pred_edge, Y_ones_edgePts),2) + tf.pow((Y_pred_edge - tf.mul(Y_pred_edge, Y_ones_edgePts)), 2))
    # tf.scalar_summary('costCtPts', cost_ctPts)


#train_op_ctPts = tf.train.AdamOptimizer(learning_rate=0.00001).minimize(cost_ctPts)
#train_op_ctPts = tf.train.AdamOptimizer(1e-4).minimize(cost_ctPts)


with tf.name_scope('costEdgePts'):
    cost_edgePts = tf.reduce_sum(tf.pow(YPred_edgePts - YReal_edgePts, 2))  # minimize squared error
    tf.scalar_summary('costEdgePts', cost_edgePts)
    train_op_edgePts = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cost_edgePts, var_list=[W_dense1, W_dense2, W_dense3, W_dense4])

with tf.name_scope('costCtPts'):
    cost_ctPts = tf.reduce_sum(tf.pow(YPred_ctPts - YReal_ctPts, 2))  # minimize squared error
    tf.scalar_summary('costCtPts', cost_ctPts)
    train_op_ctPts = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cost_ctPts, var_list=[W_dense5, W_dense6, W_dense7, W_dense8])#, B1, B2, B3, B4])

############################################# SAVE AND STORE MODEL STUFF

# Add ops to save and restore all the variables.
init_op = tf.initialize_all_variables()
# Add ops to save and restore all the variables.
saver = tf.train.Saver()
restoredFlag = 0  # always starts with 0

def restoreModel(path):
    # Restore variables from disk.
    saver.restore(sess, path)
    print("Model restored.")
    return 1

def saveModel(path):
    save_path = saver.save(sess, path)
    print("Model saved in file: %s" % save_path)

'''
def plotPredictions_ctPts():
        pred_ctPts = sess.run(YPred_ctPts, feed_dict={X: test_x, YReal_edgePts: test_edgePts, YReal_ctPts: test_ctPts})
        #plotShapes(X_test[:,:,:,0], test_ctPts, pred_ctPts, test_zmp)
        #cutout = pred_ctPts - np.multiply(pred_ctPts, test_ctPts_ones)
        #plotShapes(X_test[:, :, :, 0], pred_ctPts, test_ctPts_ones, test_zmp)
        #plotShapes(test_ctPts, pred_ctPts, cutout, test_zmp)
        #relevantPreds = np.multiply(pred_ctPts, test_ctPts_ones)
        #plotShapes(relevantPreds, test_ctPts, pred_ctPts, test_zmp)
'''

def plotPredictions_ctPts():
        pred_ctPts = sess.run(YPred_ctPts, feed_dict={X: test_x, YReal_edgePts: test_edgePts, YReal_ctPts: test_ctPts, ZMP: test_zmp_array})
        plotShapes(test_edgePts, test_ctPts, pred_ctPts, test_zmp)

def plotPredictions_edgePts():
    preds = sess.run(YPred_edgePts, feed_dict={X: test_x, YReal_edgePts: test_edgePts})
    plotShapes(test_x, test_edgePts, preds, test_zmp)


############################################# TRAIN & EVAL

# Launch the graph in a session
with tf.Session() as sess:
    print("Training edge points..")

    # Merge all the summaries and write them out to logs (by default)
    merged = tf.merge_all_summaries()
    train_writer = tf.train.SummaryWriter(logPath, sess.graph)

    # you need to initialize all variables
    sess.run(init_op)

    ##### Learn edge points

    episodes1 = 1
    bs = 32  # 64 faster convergence than 128 (lr 0.001) 32 even better with lr 0.0001
    for i in range(episodes1):

        for start, end in zip(range(0, len(train_x), bs), range(bs, len(train_x), bs)):
            sess.run(train_op_edgePts, feed_dict={X: train_x[start:end], YReal_edgePts: train_edgePts[start:end]})
        if np.mod(i, 1) == 0:
            print(i, sess.run(cost_edgePts, feed_dict={X: test_x, YReal_edgePts: test_edgePts}))
    print(i, sess.run(cost_edgePts, feed_dict={X: test_x, YReal_edgePts: test_edgePts}))

    #plotPredictions_edgePts()
    #plotPredictions_edgePts()

    ##### Learn contact points
    print("Training contact points..")

    #edgePtsAndZMP = np.zeros((train_zmp.shape[0], 100, 2))
    #train_predEdgePts = sess.run(YPred_edgePts, feed_dict={X: test_x, YReal_edgePts: test_edgePts}))
    #edgePtsAndZMP[:, :, :, 0] = train_terrain[:, :, :, 0]
    #edgePtsAndZMP[:, :, :, 1] = train_zmp_array[:, :, :, 0]

    episodes2 = 5000
    bs = 1000  # 64 lr 0.0001 8300-8400 ; 32 0.0001 bout the same; bs 128 lr 0.0001 7900s; bs 200 lr 0.0001 7900
    for i in range(episodes2):

        for start, end in zip(range(0, len(train_x), bs), range(bs, len(train_x), bs)):
            sess.run(train_op_ctPts, feed_dict={X: train_x[start:end], YReal_edgePts: train_edgePts[start:end], YReal_ctPts: train_ctPts[start:end], ZMP: train_zmp_array[start:end]})
        if np.mod(i, 1) == 0:
            print(i, sess.run(cost_edgePts, feed_dict={X: test_x, YReal_edgePts: test_edgePts}), sess.run(cost_ctPts, feed_dict={X: test_x, YReal_edgePts: test_edgePts, YReal_ctPts: test_ctPts, ZMP: test_zmp_array}))
    print(i, sess.run(cost_edgePts, feed_dict={X: test_x, YReal_edgePts: test_edgePts}), sess.run(cost_ctPts,
                                                                                                  feed_dict={X: test_x,
                                                                                                             YReal_edgePts: test_edgePts,
                                                                                                             YReal_ctPts: test_ctPts,
                                                                                                             ZMP: test_zmp_array}))

    plotPredictions_ctPts()
    plotPredictions_ctPts()


'''
    for i in range(1000):
        bs = 1280
        for start, end in zip(range(0, len(X_train), bs), range(bs, len(X_train), bs)):
            sess.run(train_op_ctPts, feed_dict={X: X_train[start:end], Y_true_edge: train_edgePts[start:end], Y_ones_edgePts: train_edgePts_ones[start:end]})

        if np.mod(i, 20) == 0:
            print(i, sess.run(cost_ctPts, feed_dict={X: X_test, Y_true_edge: test_edgePts, Y_ones_edgePts: test_edgePts_ones}))

    print(i, sess.run(cost_ctPts, feed_dict={X: X_test, Y_true_edge: test_edgePts, Y_ones_edgePts: test_edgePts_ones}))

    plotPredictions_ctPts()
    plotPredictions_ctPts()
'''