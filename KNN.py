
# We call this the Keegan Neural Network

# Because it's written by Keegan, of course.

# Things:
#  Activation function per perceptron?
#  Weights, bias...
#  NO BACKPROPOGATION - We're doing this for genetic algorithm shenanigans. If we want backprop, use TensorFlow.
#  Matrix maths? Would probably be faster than a foreach feedforward. But the network might not be fully connected, depending on evolution?
#  Not sure. We can test performance.
#  Theano is speedy for matrix shenanigans.
#  Weights Matrix * Input column vector + Bias Values
#  How can we make this work with matrices, and still add single node layers and whatnot?

# Okay, so what we're going to do-
# TODO:
#   For now, ignore matrix shenanigans. We're going to make a simple feed forward network that processes each perceptron.
#   This can be a bit ugly - we aren't using a defined number of hidden layers, so I'm going to work out an algorithm on paper and then describe it here. Pending.
#
#   FEED FORWARD - Have a queue for 'current nodes to process'
#                  Take that queue, and if the next node is waiting for another node, add it to a waiting map that has a list of nodes waiting for the provided node.
#                  After node compeletes, pop everything from that list and if it is not waiting for any OTHER nodes, then put it in the queue.
#                  This should work for arbitrary structures within the neural network, but I am one hundred percent sure that running this brain will be extraordinarily slow if it becomes large enough.
#                  However, this should allow the genetic algorithm to determine the best shape for the brain. given the inputs.
#                  

class Perceptron:
    def __init__(self):
        self.bias = random.uniform(-1, 1);


class KNN:
    def __init__(self):
        self.allo = "FFFUU";




def main():
    pass;

if (__name__ == "__main__"):
    main();
    print("Testing Keegan Neural network.");
    myPer = Perceptron();

    myKNN = KNN();
