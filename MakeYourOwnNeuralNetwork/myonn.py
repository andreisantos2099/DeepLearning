import numpy
import scipy.special
import matplotlib.pyplot
import time


#Neural Network configuration       
i_input_nodes = 784 # input node and must be 784 = (28x28 pixel image for our neural network)
i_hidden_nodes = 100
i_output_nodes = 10
f_learningrate = 0.2
i_epoch = 2
 



# This neural network based on perceptron model and it has 3 layers (1 input layer, 1 hidden layer and 1 output layer)
class cl_NeuralNetwork:

    def __init__(self, i_inputnodes, i_hiddennodes, i_outputnodes, f_learningrate):
        
        #set number of nodes(neuron) of each layer.
        self.i_inodes = i_inputnodes
        self.i_hnodes = i_hiddennodes
        self.i_onodes = i_outputnodes
        
        #set weights for each layer
        # weight input-hidden(wih)
        self.ary_wih = numpy.random.normal(0.0, pow(self.i_inodes, -0.5), (self.i_hnodes,self.i_inodes))
         # weight hidden-output(who)
        self.ary_who = numpy.random.normal(0.0, pow(self.i_hnodes, -0.5), (self.i_onodes,self.i_hnodes))       
        
        #set learning rate
        self.f_lr = f_learningrate
        
        #activation function is a sigmoid for this neural network
        self.activation_function = lambda x: scipy.special.expit(x)
 
 
        
    def func_training(self,p_lst_Training_data, p_lst_Target):
    
    
        #convert list to array 2d
        ary_Target = numpy.array(p_lst_Target, ndmin=2).T
        ary_Training_data = numpy.array(p_lst_Training_data, ndmin=2).T    
        #Training data through entire neural network.        
        #Second Layer is the hidden layer with link weights --> Xh = Weight input-hidden*Input Node 
        ary_Xhidden = numpy.dot(self.ary_wih,ary_Training_data)        
        #Sigmoid Output from Hidden Layer 
        ary_Ohidden = self.activation_function(ary_Xhidden)        
        #Last Layer is the output layer with link weights --> Ofinal = Weight hidden-out* Hidden Output Node
        Xfinal = numpy.dot(self.ary_who,ary_Ohidden)        
        #Sigmoid Output from last layer
        ary_Ofinal = self.activation_function(Xfinal) 
 
        #==== ERROR CALCULATION ======
        #Measure the Output Error => Error = Target - Output
        ary_Output_Error = ary_Target  - ary_Ofinal        
        #Backpropagate the error to previous layer
        ary_Hidden_Error = numpy.dot(self.ary_who.T, ary_Output_Error)
        pass
        
        #==== WEIGHT ADJUSTMENT ======
        #Update the weights for the links between the hidden and output layer
        self.ary_who += self.f_lr*numpy.dot((ary_Output_Error*ary_Ofinal*(1.0 - ary_Ofinal)), numpy.transpose(ary_Ohidden))        
        # Update the weights for the links between the input and hidden layer
        self.ary_wih += self.f_lr*numpy.dot((ary_Hidden_Error*ary_Ohidden*(1.0 - ary_Ohidden)), numpy.transpose(ary_Training_data))
        
           
        
        
        
        
    def func_query(self,p_lst_input):
    
        #transform Input List in 2d array dimensional
        ary_Inputs = numpy.array(p_lst_input, ndmin=2).T        
        #Second Layer is the hidden layer with link weights --> Xh = Weight input-hidden*Input Node 
        ary_Xhidden = numpy.dot(self.ary_wih,ary_Inputs)        
        #Sigmoid Output from Hidden Layer 
        ary_Ohidden = self.activation_function(ary_Xhidden)        
        #Last Layer is the output layer with link weights --> Ofinal = Weight hidden-out* Hidden Output Node
        Xfinal = numpy.dot(self.ary_who,ary_Ohidden)        
        #Sigmoid Output from last layer
        ary_Ofinal = self.activation_function(Xfinal)
        
        return ary_Ofinal
        
        
   


def func_training_NN(p_file_path):
    
 
    #load training data 
    data_file = open(p_file_path)  
    data_list = data_file.readlines()
    data_file.close()
    
    #to measure the trainning time 
    i_take_time_in = time.time()

    for e in range(i_epoch):
        # go through all records in the training data set
        for record in data_list:
            #splif the record by the "," commas
            all_values = record.split(',')
            #remove the label and rescale the values to (0.01 to 1)
            inputs = (numpy.asfarray(all_values[1:])/255*0.99)+0.01
            #create the target output values (all 0.01, except the desired label which is 0.99)
            targets = numpy.zeros(i_output_nodes) + 0.01
            # all_values[0] is the target label for this records
            targets[int(all_values[0])] = 0.99
            n.func_training(inputs,targets)

            pass
     
    #to measure the trainning time     
    i_take_time_out = time.time()
    #calculate the time spent
    i_time_spent = i_take_time_out - i_take_time_in
    print("Training time is = ", i_time_spent, "s")

   
def func_test_NN(p_file_path):

    #load  data from file
    test_data_file = open(p_file_path)
    test_data_list = test_data_file.readlines()
    test_data_file.close()
    
    # scorecard for how well the network performs, initially empty
    lst_scorecard = []
    
    #to measure the trainning time 
    i_take_time_in = time.time()

    # go through all the records in the test data set
    for record in test_data_list:
        # split the record by the ',' commas
        ary_all_values = record.split(',')
        # correct answer is first value
        i_correct_label = int(ary_all_values[0])
        # scale and shift the inputs
        ary_inputs = (numpy.asfarray(ary_all_values[1:]) / 255.0 * 0.99) + 0.01
        # query the network
        ary_outputs = n.func_query(ary_inputs)
        # the index of the highest value corresponds to the label
        i_label = numpy.argmax(ary_outputs)
        # append correct or incorrect to list
        if (i_label == i_correct_label):
            # network's answer matches correct answer, add 1 to scorecard
            lst_scorecard.append(1)
        else:
            # network's answer doesn't match correct answer, add 0 to scorecard
            lst_scorecard.append(0)
            pass
        
        pass
    #to measure the test time     
    i_take_time_out = time.time()
    #calculate the time spent
    i_time_spent = i_take_time_out - i_take_time_in
    print("Test time is = ", i_time_spent, "s")

    
    # calculate the performance score, the fraction of correct answers
    ary_scorecard  = numpy.asarray(lst_scorecard)
    print ("Performance = ", (ary_scorecard.sum() / ary_scorecard.size)*100, "%")

           
   
# main program:  

#first create a neural network class:
n = cl_NeuralNetwork(i_input_nodes,i_hidden_nodes,i_output_nodes,f_learningrate)

# Trainning data
func_training_NN("mnist_dataset/mnist_train.csv")

#Test Neural Network
func_test_NN("mnist_dataset/mnist_test_10.csv")

 
