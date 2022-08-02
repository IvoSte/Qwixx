import random
import math

def identity_activation(x):
    return x

def relu_activation(x):
    return max(0,x)

def sigmoid_activation(x):
    return  1 / (1 + math.exp(-x))

class MLP:

    def __init__(self, n_input, n_hidden, n_output, hidden_layers = 1, activation_function = sigmoid_activation, random_initialization = True, chromosome = None):
        self.n_input = n_input
        self.n_hidden = n_hidden
        self.n_output = n_output
        self.hidden_layers = hidden_layers
        self.input_weights : list(list(float)) = [] # list of lists, position 0 corresponds to the weights connecting input 1 to hidden layer 1
        self.hidden_weights : list(list(list(float))) = [] # List of lists of lists, position [0][0][0] corresponds to the weights connecting hidden layer 1, node 1 to the next hidden layer node 1
        self.output_weights : list(list(float)) = [] # 
        self.activation_function = activation_function

        if chromosome == None:
            self.init_weights(random_initialization)
        else:
            self.init_weights_with_chromosome(chromosome)


    def init_weights(self, random_flag):
        # Init input weights
        self.input_weights = [[random.random() if random_flag else 0.5 for hidden_node in range(self.n_hidden)] for input_node in range(self.n_input)]
        
        # Init output weights
        self.output_weights = [[random.random() if random_flag else 0.5 for output_node in range(self.n_output)] for hidden_node in range(self.n_hidden)]

        # For all (optional) hidden layers, initialize the hidden weights
        for hidden_layer in range(self.hidden_layers-1):
            self.hidden_weights.append([[random.random() if random_flag else 0.5 for hidden_node in range(self.n_hidden)] for hidden_node in range(self.n_hidden)])


    def init_weights_with_chromosome(self, chromosome):
        assert len(chromosome) == self.n_input + (self.hidden_layers * self.n_hidden) + self.n_output, \
            f"Chromosone length {len(chromosome)} does not match MLP specifications (i:{self.n_input} + {self.hidden_layers} * h:{self.n_hidden} + o:{self.n_output}) in MLP initialization."
        
        # Move through the flat chromosome and cut the weights from the genes -- the chromosome represents all weights in a 1D sequential list.
        start = 0
        stop = self.n_hidden
        for input_node in range(self.n_input):
            self.input_weights.append(chromosome[start:stop])
            start += self.n_hidden
            stop += self.n_hidden

        for hidden_layer_idx in range(self.hidden_layers):
            self.hidden_weights.append([])
            for hidden_node in range(self.n_hidden):
                self.hidden_weights[hidden_layer_idx].append(chromosome[start:stop])
                start += self.n_hidden
                stop += self.n_hidden

        for output_node in range(self.n_output):
            self.output_weights.append(chromosome[start:stop])
            start += self.n_hidden
            stop += self.n_hidden  


    def evaluate_input(self, input_values):
        # Make sure the input is of correct length
        assert len(input_values) == self.n_input, \
            f"Input length ({len(input_values)}) does not match number of input nodes ({self.n_input}) in input evaluation."
        
        # Calculate the values for the nodes in the first hidden layer
        hidden_layer = self.calculate_node_values(input_values, self.n_hidden, self.input_weights, self.activation_function)
        
        # Calculate the values for the nodes in all subsequent (optional) hidden layers
        for layer_idx in range(self.hidden_layers -1):
            hidden_layer = self.calculate_node_values(hidden_layer, self.n_hidden, self.hidden_weights[layer_idx], self.activation_function)
        
        # Calculate the values for the output nodes
        output_layer = self.calculate_node_values(hidden_layer, self.n_output, self.output_weights, self.activation_function)
        return output_layer


    def calculate_node_values(self, input_values, n_nodes, weights, activation):
        # Init the array
        values = [0.0 for _ in range(n_nodes)]
        
        # For all nodes in the to calculate layer
        for node_idx in range(n_nodes):

            # For all input values 
            for input_idx in range(len(input_values)):

                # Calculate the value by summing all products of the input values with the weights
                values[node_idx] += input_values[input_idx] * weights[input_idx][node_idx]

            # Activation value is caluclated by parsing the product sums through an activation function
            values[node_idx] = activation(values[node_idx])
        return values


    def __str__(self):
        return f"Input:\n{self.input_weights}\nHidden:\n{self.hidden_weights}\nOutput:\n{self.output_weights}"

if __name__ == "__main__":
    mlp = MLP(3, 5, 1, 2)
    mlp.init_weights(False)
    print(mlp.evaluate_input([1,1,1]))