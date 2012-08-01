% NN_TEMPLATE is a template 3-layer neural network for classification.
%
% Perform classification for a multi-class dataset using a neural network.
% Learn parameters with fmincg.m.
%
% Overview:
%	Read in comma-delimited data file (without header)
%	Split into training and test set
%	Specify NN parameters
%	Minimize cost function with fmincg
%	Compute performance metrics:
%		prediction accuracy on training and test sets
%		confusion matrix, sensitivity, specificity
%
% Functions used: sigmoid.m, sigmoidGradient.m, randInitializeWeights.m, nnCostFunction.m, fmincg.m, predict.m
%
% Code based on ml-class.org Ex.4
%
% To Do:
%   split data into training and test sets
%	prediction accuracy on test and training sets
%	add confusion matrix for any number of classes, specificity, sensitivity
%	allow any number of hidden layers

% Load data
data = load('dataset_01.txt');
X = data(:,1:end-1);
y = data(:,end);
m = size(X,1);

%NN layer sizes
input_layer_size = size(X,2);
hidden_layer_size = 25;
num_labels = size(unique(y),1); %output layer

%Initialize NN Parameters for the 3-layer NN
initial_Theta1 = randInitializeWeights(input_layer_size, hidden_layer_size);
initial_Theta2 = randInitializeWeights(hidden_layer_size, num_labels);

% Unroll parameters
initial_nn_params = [initial_Theta1(:) ; initial_Theta2(:)];

% Implement backprop and train network using fmincg
fprintf('\nTraining Neural Network... \n')

options = optimset('MaxIter', 40);
lambda = 0.5;

costFunction = @(p) nnCostFunction(p, ...
                                   input_layer_size, ...
                                   hidden_layer_size, ...
                                   num_labels, X, y, lambda);

[nn_params, cost] = fmincg(costFunction, initial_nn_params, options);

% Obtain Theta1 and Theta2 back from nn_params
Theta1 = reshape(nn_params(1:hidden_layer_size * (input_layer_size + 1)), ...
                 hidden_layer_size, (input_layer_size + 1));

Theta2 = reshape(nn_params((1 + (hidden_layer_size * (input_layer_size + 1))):end), ...
                 num_labels, (hidden_layer_size + 1));

%Find training set accuracy
pred = predict(Theta1, Theta2, X);
fprintf('\nTraining Set Accuracy: %f\n', mean(double(pred == y)) * 100);


