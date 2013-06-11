#!/usr/local/EPD/bin/python
#Filename: nn_helper_functions.py

#Functions used in the main nn_template.py script


import time, sys, numpy as np, scipy as sp
from numpy import log, ones, c_, r_, array, e, reshape, random, sqrt, unique, zeros, eye
from numpy import transpose as tr
from scipy import optimize as op

def sigmoid(z):
	''' (number array) -> number array
	
	Return sigmoid of input array

	'''
	g = 1./(1 + e**(-z))
	return g


def sigmoidGradient(z):
	''' (number array) -> number array
	
	Return gradient of sigmoid of input array

	'''
	if type(z) != np.ndarray: #must convert to array first
		z = array([z])
	f = 1./(1 + e**(-z))
	return f*(1-f)


def randInitializeWeights(L_in, L_out):
	''' (number arrays) -> number arrays

	Given input and output layer size, return arrays with randomly initialized numbers
	'''
	epsilon_init = 0.12
	#epsilon_init = float(sqrt(6))/sqrt(L_in + L_out)
	return np.random.rand(L_out, 1 + L_in) * 2 * epsilon_init - epsilon_init


def standardize(inp):
	''' (number array) -> number,number,number array

	Given a numeric array, return mean, standard deviation, and a normalized array.
	Subtract mean and divide by std to get the normalized array.
	'''
	mn = inp.mean(0)
	std = inp.std(0) 
	stand = (inp-mn)/std
	return mn,std,stand


def nnCostFunction(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y, lam):
	'''

	Returns cost of traversing neural net
	'''

	Theta1 = (reshape(nn_params[:(hidden_layer_size*(input_layer_size+1))],(hidden_layer_size,(input_layer_size+1))))
	
	Theta2 = (reshape(nn_params[((hidden_layer_size*(input_layer_size+1))):],(num_labels, (hidden_layer_size+1))))

	m = X.shape[0]
	n = X.shape[1]
	
	#forward pass
	y_eye = eye(num_labels)
	y_new = np.zeros((y.shape[0],num_labels))

	for z in range(y.shape[0]):
		y_new[z,:] = y_eye[int(y[z])-1]
	
	y = y_new

	a_1 = c_[ones((m,1)),X]
	z_2 = tr(Theta1.dot(tr(a_1)))

	a_2 = tr(sigmoid(Theta1.dot(tr(a_1))))
	a_2 = c_[ones((a_2.shape[0],1)), a_2]

	a_3 = tr(sigmoid(Theta2.dot(tr(a_2))))

	J_reg = lam/(2.*m) * (sum(sum(Theta1[:,1:]**2)) + sum(sum(Theta2[:,1:]**2)))

	J = (1./m) * sum(sum(-y*log(a_3) - (1-y)*log(1-a_3))) + J_reg

	#Backprop

	d_3 = a_3 - y
	
	d_2 = d_3.dot(Theta2[:,1:])*sigmoidGradient(z_2)

	Theta1_grad = 1./m * tr(d_2).dot(a_1)
	Theta2_grad = 1./m * tr(d_3).dot(a_2)

	#Add regularization

	Theta1_grad[:,1:] = Theta1_grad[:,1:] + lam*1.0/m*Theta1[:,1:]
	Theta2_grad[:,1:] = Theta2_grad[:,1:] + lam*1.0/m*Theta2[:,1:]

	#Unroll gradients
	grad = tr(c_[Theta1_grad.swapaxes(1,0).reshape(1,-1), Theta2_grad.swapaxes(1,0).reshape(1,-1)])
	
	#return statement for function testing:
	#return Theta1,Theta2, y, a_1, z_2, d_3, a_3, J, grad, Theta1_grad, Theta2_grad
	
	#optimize.fmin expects a single value, so cannot return grad
	return J


def predict(Theta1, Theta2, X):
	'''

	Return prediction of y
	'''
	m = X.shape[0]
	num_labels = Theta2.shape[0]

	h1 = sigmoid(c_[np.ones(m), X].dot(np.transpose(Theta1))) 
	h2 = sigmoid(c_[np.ones(m), h1].dot(np.transpose(Theta2)))
	
	#assign each row of output to be max of each row of h2
	y_hat = h2.argmax(1)+1
	return reshape(y_hat, (len(y_hat),1))


def pred_accuracy(Theta1, Theta2, X, y):
	'''

	Return prediction accuracy (percentage of examples classified correctly)
	'''
	p = predict(Theta1, Theta2, X)
	return np.mean(p == y)*100 


# def data_preprocess(data_filename):
# 	'''

# 	Given the name of .csv data file, return training and test sets as numpy arrays.
# 	The sets are normalized, shuffled and split according to train_frac.
# 	'''

# 	train_frac = 0.70 #fraction of data to use for training

# 	data = np.loadtxt(data_filename, delimiter = ',')	# Input: feature columns followed by dependent class column

# 	random.shuffle(data)		# shuffle rows

# 	X = array(data[:,:-1])		# separate into feature columns

# 	mn,std,X = standardize(X)	# apply feature scaling to X 


# 	y = array(data[:,-1])		# get class column
# 	y = reshape(y,(len(y),1)) 	#reshape into 1 by len(y) array

# 	# Split input file into training and test files
# 	test_rows = int(round(X.shape[0] * (1 - train_frac))) #num of rows in test set
# 	X_test = X[:test_rows, :] #test set
# 	y_test = y[:test_rows] #test set

# 	X = X[test_rows:,:] #training set
# 	y = y[test_rows:] #training set

# 	return X,y,X_test,y_test






def data_preprocess(data_filename):
	'''

	Given the name of .csv data file, return X (features) and y (class) arrays.
	The data is normalized and shuffled.
	'''

	train_frac = 0.70 #fraction of data to use for training

	data = np.loadtxt(data_filename, delimiter = ',')	# Input: feature columns followed by dependent class column

	random.shuffle(data)		# shuffle rows

	X = array(data[:,:-1])		# separate into feature columns

	mn,std,X = standardize(X)	# apply feature scaling to X 

	y = array(data[:,-1])		# get class column
	y = reshape(y,(len(y),1)) 	#reshape into 1 by len(y) array

	return X,y


def split_data(X_full, y_full, train_frac = 0.70):
	'''

	Given full feature set and class set, return split training and test sets
	'''
	# Split input file into training and test files
	test_rows = int(round(X_full.shape[0] * (1 - train_frac))) #num of rows in test set
	X_test = X_full[:test_rows, :] #test set
	y_test = y_full[:test_rows] #test set

	X = X_full[test_rows:,:] #training set
	y = y_full[test_rows:] #training set

	return X,y,X_test,y_test







def nn_train(X,y,lam = 1.0, hidden_layer_size = 10):
	'''

	Train neural network and return parameters Theta1, Theta2
	'''
		
	# NN input and output layer sizes
	input_layer_size = X.shape[1]
	num_labels = unique(y).shape[0] #output layer

	# Initialize NN parameters
	initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size)
	initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels)

	#non-random initalization for testing:
	#initial_Theta1 = 0.5*ones((hidden_layer_size, 1+input_layer_size))
	#initial_Theta2 = 0.5*ones((num_labels, 1+hidden_layer_size))


	# Unroll parameters
	initial_nn_params = np.append(initial_Theta1.flatten(1), initial_Theta2.flatten(1))
	initial_nn_params = reshape(initial_nn_params,(len(initial_nn_params),)) #flatten into 1-d array


	# Find and print initial cost:
	J_init = nnCostFunction(initial_nn_params,input_layer_size,hidden_layer_size,num_labels,X,y,lam)
	print 'Initial cost: ' + str(J_init)

	# Implement backprop and train network, run fmin
	print 'Training Neural Network...'
	print 'fmin results:'

	#nn_params, cost, _, _, _  = op.fmin(lambda t: nnCostFunction(t, input_layer_size, hidden_layer_size, num_labels, X, y, lam), initial_nn_params, xtol = 0.01, ftol = 0.01, maxiter = 500, full_output=1)

	nn_params, cost, _, _, _  = op.fmin_cg(lambda t: nnCostFunction(t, input_layer_size, hidden_layer_size, num_labels, X, y, lam), initial_nn_params, gtol = 0.001, maxiter = 40, full_output=1)
		

	Theta1 = (reshape(nn_params[:(hidden_layer_size*(input_layer_size+1))],(hidden_layer_size,(input_layer_size+1))))
		
	Theta2 = (reshape(nn_params[((hidden_layer_size*(input_layer_size+1))):],(num_labels, (hidden_layer_size+1))))

	return Theta1, Theta2	