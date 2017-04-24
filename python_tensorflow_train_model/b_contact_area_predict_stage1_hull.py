#!/usr/bin/env python
import os
import scipy.io
import sys
import time

from utils import myCnnUtils
from utils import myUtils
import numpy as np
import tensorflow as tf

from utils import myDataLoader as myLoader

#############################################
#
#   This script uses tensorflow to train a model to
#   make a prediction of a convex hull,
#   given the uneven terrain under a non-convex foot shape.
#
#   Instead of the deterministic convex hull algorithm,
#   this method is probabilistic and might make a faster prediction but is less accurate (trade off).
#
#   The ground truth is a map of triangles, each triangle has a different class number.
#   Each point in the triangle has the same class number.
#   The goal is to get the memberships of the points to the triangles right.
#
#   This network is used as stage 1 in the contact area prediction (not the contact points prediction).
#
############################################# CONFIG

dataWidth = 20
dataHeight = 20
dataLen = dataWidth*dataHeight

clsIdx1 = 400
clsIdx2 = 402

trainTestSplit = 66
bs = 128
learningRate = 0.001
episodes = 5000
# 128 0.0001 best so far

############################################# Directories for models, logging, etc

script_name = os.path.basename(sys.argv[0]).replace(".py", "")
timeStr = time.strftime('%m_%d_%H_%M')  # easy to sort by filename
path = "generated_models/trck_hull_"+script_name
myUtils.myMakeDir(path)
dirpath = path+"/run_"+timeStr
myUtils.myMakeDir(dirpath)
path = dirpath +"/track_hull_"+timeStr+".ckpt"
plotPath = dirpath +"/track_hull_"+timeStr+"_plot_"
tempModelPath = dirpath +"/track_hull_"+timeStr+"_model_"
logPath = "generated_logs/track_hull_"+script_name+"/logs_hull_"+timeStr
myUtils.myMakeDir(logPath)

############################################ LOAD DATA (several parts)

filePartName = 'training_data/predict_triangle_two_stages/data_hull_part'
fileEnding = '.mat'
matName = 'data'
numParts = 5
data = [];

for i in range(numParts):
    fn = filePartName+str(i+1)+fileEnding
    mat = scipy.io.loadmat(fn)
    data_part = mat[matName]
    if(len(data) > 0):
        data = np.concatenate((data, data_part), axis=0)
    else:
        data = data_part

train, test = myLoader.splitData(data, trainTestSplit)

train_terrain, train_cls = myLoader.separateXY(train, clsIdx1)
test_terrain, test_cls = myLoader.separateXY(test, clsIdx1)

trainSetSize = train.shape[0]
testSetSize = test.shape[0]

############################################# HELPER FUNCTIONS

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def restoreModel(saver, sess, path):
    # Restore variables from disk.
    saver.restore(sess, path)
    print("Model restored.")
    return 1

def saveModel(saver, sess, path):
    save_path = saver.save(sess, path)


############################################# DEFINE COMPUTATION GRAPH
########## Network to predict a map of triangle class values

# Input X
# [bathSizeUnspecified, height, width, channels(e.g. rgb)]
X = tf.placeholder("float", [None, 400])

# Ground truth place holder
Y_ = tf.placeholder("float", [None, 400])

W_dense1 = weight_variable([400, 400])
featMap4 = tf.matmul(X, W_dense1)
featMap4 = tf.nn.relu(featMap4)

W_dense2 = weight_variable([400, 400])
featMap5 = tf.matmul(featMap4, W_dense2)
featMap5 = tf.nn.relu(featMap5)

W_dense3 = weight_variable([400, 400])
featMap6 = tf.matmul(featMap5, W_dense3)
featMap6 = tf.nn.relu(featMap6)

W_dense7 = weight_variable([400, 400])
featMap10 = tf.matmul(featMap6, W_dense7)
featMap10 = tf.nn.relu(featMap10)

Y_pred = featMap10


############################################# COST FUNCTION and OPTIMIZER

# TODO model costfunction such that the actual value of the class does not matter, only the class memberships
# COST FUNCTION
cost = tf.reduce_sum(tf.pow(Y_pred - Y_, 2))  # minimize squared error between prediction and ground_ truth
train_op = tf.train.AdamOptimizer(learning_rate=learningRate).minimize(cost)

# cost for error eval printing with mean
cost_mean = tf.reduce_mean(tf.pow(Y_pred - Y_, 2))  # minimize squared error


############################################# SAVE AND STORE MODEL STUFF


def plots(name, sess):
    preds = sess.run(Y_pred, feed_dict={X:test_terrain, Y_: test_cls})
    myCnnUtils.plotShapes_2(test_terrain, test_cls, preds, dataWidth, dataHeight, plotPath + name)

# always initialize the tensorflow variables
init_op = tf.initialize_all_variables()
saver = tf.train.Saver()
restoredFlag = 0  # always starts with 0


############################################# TRAIN & EVAL

def train(sess):
    sess.run(init_op)

    for i in range(episodes):

        # train with whole training set in batches
        for start, end in zip(range(0, trainSetSize, bs), range(bs, trainSetSize, bs)):
            terrain = train_terrain[start:end]
            cls = train_cls[start:end]
            sess.run(train_op, feed_dict={X: terrain, Y_: cls})

        if np.mod(i, 100) == 0:
            trainingError = sess.run(cost, feed_dict={X: terrain, Y_: cls})
            testSetError = sess.run(cost, feed_dict={X:test_terrain, Y_: test_cls})

            trainingError_mean = sess.run(cost_mean, feed_dict={X: terrain, Y_: cls})
            testSetError_mean = sess.run(cost_mean, feed_dict={X:test_terrain, Y_: test_cls})
            print i, 'mse train:', trainingError_mean, 'mse test:', testSetError_mean, 'se train:', trainingError, 'se test:', testSetError

            preds = sess.run(Y_pred, feed_dict={X:test_terrain, Y_: test_cls})
            myCnnUtils.plotShapes_2(test_terrain, test_cls, preds, dataWidth, dataHeight, plotPath + str(i))

            # save model
            iter_path = tempModelPath +str(i)+".ckpt"
            saveModel(saver, sess, iter_path)

    print(i, sess.run(cost, feed_dict={X:test_terrain, Y_: test_cls}))



############################################# MAKE PREDICTIONS
def start_training():
    with tf.Session() as sess:

        finalModelPath = tempModelPath + "final_model.ckpt"
        print 'PARAMETERS:', 'LR:', learningRate, 'BS:', bs, 'method', train_op.name
        print("Training...")
        print("Model: %s" % finalModelPath)

        train(sess)

        saveModel(saver, sess, finalModelPath)
        print("Model saved in file: %s" % finalModelPath)



############################################# MAKE PREDICTIONS

def makePreds(input_x):
    with tf.Session() as sess:

        # choose the best model for the predictions:
        fileName = "generated_models/trck_hull_nn_hull_oldstuff/run_10_20_16_22/track_hull_10_20_16_22_model_4700.ckpt" #12 or so test error
        restoredFlag = restoreModel(saver, sess, fileName)

        print 'PARAMETERS:', 'LR:', learningRate, 'BS:', bs, 'method', train_op.name

        return sess.run(Y_pred, feed_dict={X: input_x})

