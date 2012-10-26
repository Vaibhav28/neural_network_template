Neural Network Template
==

Intro
--
A 3-layer neural network template for classification, implemented in MATLAB and python.

Constraints
--
Network is suitable for data with continuous independent variables and a dependent variable designating 2 or more classes.

Each data row must be complete (no missing values).

Features must be numerical (continuous).	

Classes must be designated with consecutive integers, starting from 1 (for example, {1,2,3,4} but not {1,2,4}). 
Every class must be represented in the training set.
Due to Octave/MATLAB syntax, '0' cannot be used to designate a class.

Notes
--
Output layer uses sigmoid as activation function.

Regression parameters are learned by minimizing a cost function with fmincg or fminunc (MATLAB/Octave) and fmin_cg (python).

Script splits input data file into training and test sets, and computes some performance metrics after the network is trained. These are test and training set prediction accuracy and confusion matrix.

Code is based on Ex.4 of ml-class.org.

Datasets used:
--
*Fisher's Iris: http://archive.ics.uci.edu/ml/datasets/Iris
*Wine: http://archive.ics.uci.edu/ml/datasets/Wine
*Breast Cancer Wisconsin (Diagnostic): http://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)

Dataset processing steps: 
	Labels of "0" in these datasets have been replaced with non-zero values to accomodate MATLAB/Octave syntax.
	Classes in Wine dataset were relabeled to consecutive integers. The class column has been moved to the last column in the dataset.
	Classes in Breast Cancer dataset were relabeled to 1 (malignant) and 2 (benign). Class column has been moved to the end.

Files:

nn_template.py: python implementation script

nn_template.m: MATLAB/Octave implementation script (working)
sigmoid.m, sigmoidGradient.m, randInitializeWeights.m, nnCostFunction.m, fmincg.m, predict.m: functions used by main .m script