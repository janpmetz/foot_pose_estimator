#!/usr/bin/env python
import os
import sys
import time

import matplotlib.pyplot as plt
from utils import myCnnUtils
from utils import myUtils
import numpy as np
import tables
import tensorflow as tf

from utils import myDataLoader as myLoader

#############################################
#
#   This script uses tensorflow to train a model to
#   predict the pitch of the foot
#   given the uneven terrain under a non-convex foot shape.
#
############################################# CONFIG

dataWidth = 30
dataHeight = 30
dataLen = dataWidth*dataHeight
scale = 9

# todo store this in the file
num_parts = 19
partSetSize = 50000
cls_idxs = [900, 902, 903, 904, 905, 906, 907]

############################################# Directories for models, logging, etc

keyword = "triangle"
script_name = os.path.basename(sys.argv[0]).replace(".py", "")
timeStr = time.strftime('%m_%d_%H_%M')  # easy to sort by filename
path = "generated_models/"+keyword+"_"+script_name
myUtils.myMakeDir(path)
path = path +"/"+keyword+"_"+timeStr+".ckpt"
logPath = "generated_logs/"+keyword+"_"+script_name+"/logs_"+keyword+"_"+timeStr
myUtils.myMakeDir(logPath)


partName = '../training_data/parts2/data_ps_'
fileEnding = '.h5'

############################################# HELPER FUNCTIONS

def getPart(part_id):
    file_handle = tables.openFile(partName+str(part_id)+fileEnding, mode='r')
    return file_handle

def closePart(part_id):
    tables.openFile(partName + str(part_id) + fileEnding)


def getbatch(file_handle, start, fin):
    data = file_handle.root.data[:, start:fin]
    data = np.transpose(data)
    [terrain, zmp, roll, pitch, c1, c2, c3, maxScale] = myLoader.split_by_idxs(data, cls_idxs)

    terrain = terrain.reshape(-1, dataWidth, dataHeight, 1)
    zmp = zmp - 1 # matlab starts with 1, but numpy with 0
    pitch = np.nan_to_num(pitch)
    #roll = np.nan_to_num(roll)
    #c1 = c1 - 1
    #c2 = c2 - 1
    #c3 = c3 - 1
    #cps = np.concatenate([c1, c2, c3], axis=1)
    #cps = cps / 100 # magnitude?
    #myUtils.setElems(terrain, zmp, zmpVal)
    return terrain, zmp, pitch, maxScale

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
########## Network to predict the pitch

X = tf.placeholder("float", [None, dataWidth, dataHeight, 1])
ZMP = tf.placeholder("float", [None, 2])
Y_ = tf.placeholder("float", [None, 1])   # 3 contact coordinates

W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])
fm = tf.nn.conv2d(X, W_conv1, strides=[1, 5, 5, 1], padding='SAME') + b_conv1
fm = tf.nn.relu(fm)
#fm = tf.nn.max_pool(fm, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

W_conv2 = weight_variable([4, 4, 32, 64])
b_conv2 = bias_variable([64])
fm = tf.nn.conv2d(fm, W_conv2, strides=[1, 4, 4, 1], padding='SAME') + b_conv2
fm = tf.nn.relu(fm)
#fm = tf.nn.max_pool(fm, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# zmp
#W_zmp = weight_variable([2, 16])
#B_zmp = bias_variable([16])
#fm_zmp = tf.matmul(ZMP, W_zmp) + B_zmp
#fm_zmp = tf.nn.relu(fm_zmp)

# put them together
len = 2*2*64
fm = tf.reshape(fm, [-1, len])
fm = tf.concat(1, [ZMP, fm])

# dense
#len = 256
#fm = tf.reshape(fm, [-1, len])
W5 = weight_variable([len+2, 1024])
B5 = bias_variable([1024])
fm = tf.matmul(fm, W5) + B5
fm = tf.nn.relu(fm)

W6 = weight_variable([1024, 256])
B6 = bias_variable([256])
fm = tf.matmul(fm, W6) + B6
fm = tf.nn.relu(fm)

W7 = weight_variable([256, 64])
B7 = bias_variable([64])
fm = tf.matmul(fm, W7) + B7
fm = tf.nn.relu(fm)

W11 = weight_variable([64, 1])
B11 = bias_variable([1])
fm = tf.matmul(fm, W11) + B11

#keep_prob = tf.placeholder(tf.float32)
#h_fc1_drop = tf.nn.dropout(fm, keep_prob)

#Readout Layer
#Finally, we add a softmax layer, just like for the one layer softmax regression above.

#W_fc2 = weight_variable([1024, 100])
#b_fc2 = bias_variable([100])
#fm = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)


#fm = tf.nn.relu(fm)

#fv = tf.reshape(X, [-1, 900])
#W1 = weight_variable([900, 900])
#B1 = bias_variable([900])
#fm = tf.matmul(fv, W1) + B1
#fm = tf.nn.relu(fm)
#fm = tf.reshape(X, [-1, 30,30,1])

#fm = tf.nn.max_pool(X, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
#fm = tf.nn.max_pool(fm, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

Y_pred = fm

############################################# COST FUNCTION and OPTIMIZER


cost = tf.reduce_mean(tf.pow(Y_pred - Y_, 2))  # minimize squared error
train_op = tf.train.AdamOptimizer(learning_rate=0.0001).minimize(cost)

meanAbsError = tf.reduce_mean(tf.abs(Y_pred - Y_))  # minimize squared error


############################################# SAVE AND STORE MODEL STUFF

# todo plooooots
def plots(terrain_test, cps_test):
    preds = sess.run(Y_pred, feed_dict={X:terrain_test, Y_: cps_test})
    myCnnUtils.plotShapes_pts(terrain_test, cps_test, preds, dataWidth, dataHeight)

init_op = tf.initialize_all_variables()
saver = tf.train.Saver()
restoredFlag = 0  # always starts with 0

############################################# TRAIN & EVAL

def train():
    sess.run(init_op)

    bs = 128  # but yxou need to measure this whith the MEAN error not just thge sum
    episodes = 3
    reps = 10

    for repetition in range(reps):
        print 'repetition', repetition

        for i in range(episodes):
            for part_i in range(num_parts):
                part_file_handle = getPart(part_i)

                for start, end in zip(range(0, partSetSize, bs), range(bs, partSetSize, bs)):
                    terrain, zmp, pitch, maxScale = getbatch(part_file_handle, start,end)
                    sess.run(train_op, feed_dict={X: terrain, ZMP: zmp, Y_: pitch})

                test_part_file_handle = getPart('test')
                terrain_test, zmp_test, pitch_test, maxScale = getbatch(test_part_file_handle, 10000, 10000*2)
                trainingError = sess.run(cost, feed_dict={X: terrain, ZMP: zmp, Y_: pitch})
                testSetError = sess.run(cost, feed_dict={X:terrain_test, ZMP: zmp_test, Y_: pitch_test})

                print repetition, i, part_i, 'se train:', trainingError, 'se test:', testSetError

                preds = sess.run(Y_pred, feed_dict={X: terrain_test, ZMP: zmp_test, Y_: pitch_test})

                # rescale
                preds *= scale;
                pitch_test *= scale;
                print('real ', pitch_test[0], 'pred', preds[0])
                print('real ', pitch_test[1], 'pred', preds[1])
                print('real ', pitch_test[2], 'pred', preds[2])

        saveModel(saver, sess, path)


with tf.Session() as sess:
    #fileName = "models/triangle_nn_triangle_parts_pitch_2/triangle_11_07_14_03.ckpt"
    #restoredFlag = restoreModel(saver, sess, fileName)

    if restoredFlag == 0:
        print("Training...")
        print("Model: %s" % path)
        #fig = plt.figure(1)
        plt.ion()
        #plt.show(block=False)
        train()
        saveModel(saver, sess, path)
        print("Model saved in file: %s" % path)

    #test_part_file_handle = getPart('verify_with_maxscale')
    test_part_file_handle = getPart('test')

    terrain_test, zmp_test, pitch_test, maxScale = getbatch(test_part_file_handle, 10000, 10000*2)

    meanAbsError = sess.run(meanAbsError, feed_dict={X:terrain_test, ZMP: zmp_test, Y_: pitch_test})
    print'meanAbsError test:', meanAbsError

    preds = sess.run(Y_pred, feed_dict={X: terrain_test, ZMP: zmp_test, Y_: pitch_test})

    #rescale
    preds *= scale;
    pitch_test *= scale;

    print('real ', pitch_test[0], 'pred', preds[0])
    print('real ', pitch_test[1], 'pred', preds[1])
    print('real ', pitch_test[2], 'pred', preds[2])
    print('real ', pitch_test[3], 'pred', preds[3])

    for i in range(100):
        print('real ', pitch_test[i], 'pred', preds[i])


    #other_plots(terrain_test, cps_test)
    #other_plots(test_terrain, test_cls)
    #other_plots(test_terrain, test_cls)
    #other_plots(test_terrain, test_cls)



