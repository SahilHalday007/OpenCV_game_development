import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class Neuron:
    def __init__(self, weights, bias):
        self.weights = weights
        self.bias = bias

    def feed_forward(self, inputs):
        total = np.dot(self.weights, inputs) + self.bias

        return sigmoid(total)


class NeuralNetwork:
    def __init__(self):
        weights = np.array([0, 1])
        bias = 4

        self.h1 = Neuron(weights, bias)
        self.h2 = Neuron(weights, bias)
        self.o1 = Neuron(weights, bias)

    def feed_forward(self, x):
        out_h1 = self.h1.feed_forward(x)
        out_h2 = self.h2.feed_forward(x)
        out_o1 = self.o1.feed_forward(np.array([out_h1, out_h2]))

        return out_o1

network = NeuralNetwork()
x = np.array([0, 1])

print(network.feed_forward(x))