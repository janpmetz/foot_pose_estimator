# Multi contact point foot pose estimator

The pose estimator makes a prediction of how a foot stands on uneven terrain, where the foot shape can be non-convex.
<<<<<<< Updated upstream
=======

The framework contains three machine learning approaches to estimate the pose and one approach to calculate the pose deterministically using a non-convex hull algorithm.

The best approach, the multi-contact-point-estimator and the deterministic algorithm are then implemented in ROS to make a path planning simulation.

The framework consists of four parts:
>>>>>>> Stashed changes

The framework contains three machine learning approaches to estimate the pose using neural networks and one approach to calculate the pose deterministically using a non-convex hull algorithm.

+ Multi contact point estimation
+ Contact area triangle estimation
+ Pitch estimation
+ Deterministic pose calculation

The best approach, the multi-contact-point-estimator, and the deterministic algorithm are then implemented in ROS to make a path planning simulation.

The framework consists of four parts:

#### Generate training data in Matlab

#### Train a model in Python with Tensorflow

#### Compile a library to load and run the trained model file in other projects

#### Implementation in ROS to run a path planning simulation using the model


