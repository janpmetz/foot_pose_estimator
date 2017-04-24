#!/usr/bin/env python
import os
import scipy.io
import sys
import time

from utils import myCnnUtils
from utils import myUtils
import numpy as np
import tensorflow as tf

import b_contact_area_predict_stage1_hull as hullPrediction
from utils import myDataLoader as myLoader

############################################# STAGE 2
#
#   This script uses tensorflow to train a model to
#   make a prediction of the contact AREA as a triangle,
#   given the predicted probabilistic convex hull (of uneven terrain under a non-convex foot shape).
#
#   Instead of the deterministic convex hull algorithm,
#   this method uses a probabilistic convex hull algorithm and might make a faster prediction but is less accurate.
#   The model to predict the hull is trained first (as stage 1).
#
############################################# CONFIG

trainTestSplit = 66
dataWidth = 20
dataHeight = 20
dataLen = dataWidth*dataHeight

clsIdxs = [400,800]

bs = 1280
learningRate = 0.0001
episodes = 5000
# 128 0.0001 best so far

############################################# Directories for models, logging, etc

script_name = os.path.basename(sys.argv[0]).replace(".py", "")
timeStr = time.strftime('%m_%d_%H_%M')  # easy to sort by filename
path = "generated_models/trck_hull_triangle_"+script_name
myUtils.myMakeDir(path)
dirpath = path+"/run_"+timeStr
myUtils.myMakeDir(dirpath)
path = dirpath +"/track_hull_"+timeStr+".ckpt"
plotPath = dirpath +"/track_hull_"+timeStr+"_plot_"
tempModelPath = dirpath +"/track_hull_"+timeStr+"_model_"
logPath = "logs/track_hull_"+script_name+"/logs_hull_"+timeStr
myUtils.myMakeDir(logPath)


############################################ # LOAD DATA (several parts)

filePartName = 'training_data/predict_triangle_two_stages/data_triangleMap_'
fileEnding = '.mat'
matName = 'data'
numParts = 7
data = [];

for i in range(numParts):
    fn = filePartName+str(i+1)+fileEnding
    mat = scipy.io.loadmat(fn)
    data_part = mat[matName]
    if(len(data) > 0):
        data = np.concatenate((data, data_part), axis=0)
    else:
        data = data_part


# verify
mat_check = scipy.io.loadmat('training_data/predict_triangle_two_stages/data_triangleMap_verify.mat')
data_verify = mat_check[matName]

train, test = myLoader.splitData(data, trainTestSplit)

[train_terrain, train_cls, train_zmp] = myLoader.split_by_idxs(train, clsIdxs)
[test_terrain, test_cls, test_zmp] = myLoader.split_by_idxs(test, clsIdxs)

################################################# Get the hull predictions

train_hull = hullPrediction.makePreds(train_terrain)
test_hull = hullPrediction.makePreds(test_terrain)

def normit(data):
    for i in range(data.shape[0]):
        data[i, :] = data[i, :] / data[i, :].max()

normit(train_hull)
normit(test_hull)

trainSetSize = train.shape[0]
testSetSize = test.shape[0]

#reshape zmp as 1 index number (comes from matlab that starts counting from 1 not 0 like python)
train_zmp = ((train_zmp[:,0]-1) * dataWidth) + train_zmp[:,1] #wait does the zmp start with 0
test_zmp = ((test_zmp[:,0]-1) * dataWidth) + test_zmp[:,1] #wait does the zmp start with 0


def setZmp(data, zmp):
    zmpVal = 5
    zmpint = zmp.astype(int)
    for i in range(data.shape[0]):
        data[i, zmpint[i]] = zmpVal

setZmp(train_hull, train_zmp)
setZmp(test_hull, test_zmp)

train_zmp = np.reshape(train_zmp, (-1,1))
test_zmp = np.reshape(test_zmp , (-1,1))


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
########## Network to predict a map with the contact area as a triangle

# Input X
# [bathSizeUnspecified, height, width, channels(e.g. rgb)]
X = tf.placeholder("float", [None, 400])

# Ground truth place holder
Y_ = tf.placeholder("float", [None, 400])

ZMP = tf.placeholder("int64", [None, 1])

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

W_dense8 = weight_variable([400, 400])
featMap10 = tf.matmul(featMap10, W_dense8)
featMap10 = tf.nn.relu(featMap10)

Y_pred = featMap10


############################################# COST FUNCTION and OPTIMIZER

# COST FUNCTION
cost = tf.reduce_sum(tf.pow(Y_pred - Y_, 2))  # minimize squared error
#train_op = tf.train.AdamOptimizer(learning_rate=learningRate).minimize(cost)
train_op = tf.train.RMSPropOptimizer(learning_rate=learningRate).minimize(cost)
cost_mean = tf.reduce_mean(tf.pow(Y_pred - Y_, 2))  # minimize squared error


############################################# SAVE AND STORE MODEL STUFF

def plots(x, y, z, name):
    preds = sess.run(Y_pred, feed_dict={X:x, Y_: y, ZMP: z})
    myCnnUtils.plotShapes_2_andZMP(x, y, preds, dataWidth, dataHeight, plotPath + name, z)


init_op = tf.initialize_all_variables()
print '+++ ONLY RESTORING VARIABLE W_dense1, 2, 3, 7, 8+++'
saver = tf.train.Saver([W_dense1, W_dense2, W_dense3, W_dense7, W_dense8])
restoredFlag = 0  # always starts with 0


############################################# TRAIN & EVAL

def train(x_train, x_test, y_train, y_test, z_train, z_test):
    sess.run(init_op)

    for i in range(episodes):

        # train with whole training set in batches
        for start, end in zip(range(0, trainSetSize, bs), range(bs, trainSetSize, bs)):
            terrain = x_train[start:end]
            cls = y_train[start:end]
            zmp = z_train[start:end]
            train_dict = {X: terrain, Y_: cls, ZMP: zmp}
            sess.run(train_op, feed_dict=train_dict)

        test_dict = {X: x_test, Y_: y_test, ZMP: z_test}

        if np.mod(i, 100) == 0:
            trainingError = sess.run(cost, feed_dict=train_dict)
            testSetError = sess.run(cost, feed_dict=test_dict)

            trainingError_mean = sess.run(cost_mean, feed_dict=train_dict)
            testSetError_mean = sess.run(cost_mean, feed_dict=test_dict)
            print i, 'mse train:', trainingError_mean, 'mse test:', testSetError_mean, 'se train:', trainingError, 'se test:', testSetError

            preds = sess.run(Y_pred, feed_dict=test_dict)
            myCnnUtils.plotShapes_2_andZMP(test_dict.get(X), test_dict.get(Y_), preds, dataWidth, dataHeight, plotPath + str(i), test_dict.get(ZMP))

            iter_path = tempModelPath +str(i)+".ckpt"
            saveModel(saver, sess, iter_path)

    print(i, sess.run(cost, feed_dict=test_dict))



with tf.Session() as sess:
    #fileName = "models/trck_hull_nn_hull/track_hull_06_18_14_24.ckpt"
    #fileName = "models/trck_hull_nn_hull_oldstuff/track_hull_10_14_21_03.ckpt"

    #fileName = "models/trck_hull_nn_hull_oldstuff/run_10_20_14_12/track_hull_10_20_14_12.ckpt" #12 or so test error
    #restoredFlag = restoreModel(saver, sess, fileName)

    finalModelPath = tempModelPath + "final_model.ckpt"

    print 'PARAMETERS:', 'LR:', learningRate, 'BS:', bs, 'method', train_op.name

    '''
    text_file = open(dirpath + "/params.txt", "w")
    text_file.write("lr: %s \n" % learningRate)
    text_file.write("bs: %s \n" % bs)
    text_file.write("method: %s \n" % train_op.name)
    text_file.close()

    #if restoredFlag == 0:
    print("Training... from hull to triangle")
    print("Model: %s" % finalModelPath)
    train(train_hull, test_hull, train_cls, test_cls, train_zmp, test_zmp)
    saveModel(saver, sess, finalModelPath)
    print("Model saved in file: %s" % finalModelPath)
    #
    '''


    ########################
    # verify some stuff
    verify_terrain, verify_cls, verify_zmp = myLoader.my3SplitData(data_verify, clsIdx1, clsIdx1 * 2)
    verify_hull = hullPrediction.makePreds(verify_terrain)
    normit(verify_hull)
    verify_zmp = ((verify_zmp[:, 0] - 1) * dataWidth) + verify_zmp[:, 1]  # wait does the zmp start with 0
    setZmp(verify_hull, verify_zmp)
    verify_zmp = np.reshape(verify_zmp, (-1, 1))

    fileName = "generated_models/trck_hull_triangle_combo_stages/run_10_23_19_52/track_hull_10_23_19_52_model_1600.ckpt" #12 or so test error
    restoredFlag = restoreModel(saver, sess, fileName)

    plots(verify_hull, verify_cls, verify_zmp, "verify_1")
    plots(verify_hull, verify_cls, verify_zmp, "verify_2")
    plots(verify_hull, verify_cls, verify_zmp, "verify_3")
    plots(verify_hull, verify_cls, verify_zmp, "verify_4")
    plots(verify_hull, verify_cls, verify_zmp, "verify_5")

    plots(test_hull, test_cls, test_zmp, "final_1")
    plots(test_hull, test_cls, test_zmp, "final_2")
    plots(test_hull, test_cls, test_zmp, "final_3")


