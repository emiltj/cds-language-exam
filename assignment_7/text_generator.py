#!/usr/bin/python

'''
###############################################################
--------------- Import of modules and libraries ---------------
###############################################################
'''
import pandas as pd
import numpy as np
import os, string, argparse
import matplotlib.pyplot as plt
from random import sample
from itertools import groupby
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.losses import categorical_crossentropy
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

'''
###############################################################
------------ Defining functions to be used in main ------------
###############################################################
'''
def text_processing(token_list):
    '''
    Function for processing a list of tokens. Removes punctuation and makes to lowercase.
    
    token_list: A list of tokens
    '''
    # Create a table for making a "translation" for all punctuations
    table = str.maketrans("", "", string.punctuation)
    
    # Apply the translation
    token_list = [token.translate(table) for token in token_list] # For token in tokens return the token after applying the translation using the table
    
    # Remove non-alphanumeric characters and convert to lowercase
    token_list = [token.lower() for token in token_list if token.isalpha()]

    # Return the processed token list
    return token_list

def get_sequences_running_window(token_list, window_size, window_step_length):
    '''
    Function for retrieving sequences of tokens in a list of tokens. Uses a moving window and saves a sequence for each window step.
            
    token_list: A list of tokens
    window_size: Size of the window -> determines the length of the sequences
    window_step_length: Step length of the window.     
    
    Example:
    Input: tokenlist = ["once", "upon", "a", "time", "in"], window_size = 3, window_step_length = 1
    Output: [["once upon a"], ["upon a time"], ["a time in"]]
    '''
    # Empty list for appending the sequences for each window
    sequences = []
    
    # For every number in a range of numbers
    # e.g. [window_size, window_size+1, window_size+3, window_size+3 ...] (up until) length of token list
    for i in range(window_size, len(token_list), window_step_length):
        
        # Define a sequence, which are tokens: i minus window_size to window_size. (e.g. [51-51: 51] -> [0:51])
        sequence = token_list[i-window_size:i]
        
        # Join this sequence of individual tokens to a single string:
        sequence = " ".join(sequence)
        
        # Append the sequence to list of sequences
        sequences.append(sequence)

    # Return the list of sequences
    return sequences

def vectorize_sequences(sequences):
    '''
    Function that vectorizes sequences. The vectors correspond to an ID that is saved in the tokenizer.
    
    sequences: A list of sequences. E.g. [["once upon a"], ["upon a time"], ["a time in"]]
    '''
    
    # Initialize tokenizer
    tokenizer = Tokenizer(filters = "")

    # Fit tokenizer to text (having every unique word assigned an integer for the model)
    tokenizer.fit_on_texts(sequences)

    # Have the sequences as integers (in a numpy array)
    sequences_int = np.array(tokenizer.texts_to_sequences(sequences))
    
    # Return sequences as vectors, and the tokenizer (to be able to convert from integers back to words again)
    return sequences_int, tokenizer

def model_init(vocabulary_length, sequence_length, lstmlayers):
    '''
    Function that initializes the model used in the script
    
    vocabulary_length: Number of unique words in the texts
    sequence_length: Length of the sequences. Used as input shape for the model
    lstmlayers: Number and size of LSTM layers. E.g. [128, 128]
    '''
    
    # Initialize sequential
    model = Sequential()

    # Add embedding layer
    model.add(Embedding(vocabulary_length, # Input dimensions should be length of vocabulary
                        sequence_length, # Output dimensions should be length of each of the sequences
                        input_length = sequence_length)) # Input length, is also length of each of the sequences

    # Add LSTM layers
    for i in range(1, len(lstmlayers)+1):
        
        # If the LSTM layer is not the last layer, then include "return_sequences = True" as input for the next layer
        if i < len(lstmlayers):
            model.add(LSTM(lstmlayers[i-1], 
                           return_sequences = True))
            
        # If the LSTM layer is the last, do not include return sequences.
        if i == len(lstmlayers):
            model.add(LSTM(lstmlayers[i-1]))        

    # Add dense layer
    model.add(Dense(32, 
                    activation = "relu"))

    # Add final dense layer
    model.add(Dense(vocabulary_length, # Output dimensions being the number of different options for predictions
                   activation = "softmax")) # Use softmax to get output predictions as probabilities

    # Define optimizer
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
    
    # Compile model
    model.compile(loss = categorical_crossentropy, optimizer = optimizer, metrics = ["accuracy"])
    
    # Return the model
    return model

def plot_history(H, epochs, outpath):
    """
    Function which plots accuracy and loss over epochs (courtesy of Ross McLachlan)
    
    H: model history
    epoch: Number of epochs the model was trained with
    outpath: Outpath for saving the training history
    """
    # Visualizing performance
    plt.style.use("fivethirtyeight")
    plt.figure()
    plt.plot(np.arange(0, epochs), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, epochs), H.history["accuracy"], label="train_acc")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, format='png', dpi=100)

def generate_sequences(model, tokenizer, sequence_length, seed_sequence, generated_sequence_length):
    '''
    Function that creates a new generated sequence using the predictions of a trained model.
    
    model: Model for which to use to generate sequences
    tokenizer: A fitted tokenizer for retrieving words from integers
    sequence_length: Length of the text sequences - to get correct format for the model
    seed_sequence: Starting word for the model to predict from
    generated_sequence_length: Specifies the wanted length of the generated sequence
    '''
    
    # Empty list for appending the individual tokens of the generated text
    generated_text = []
    
    # Go through below loop, until the wanted generated sequence length has been met
    for _ in range(generated_sequence_length):
        
        # Encode the seed text as an integer - with the integer matching the index in the trained tokenizer
        encoded = tokenizer.texts_to_sequences([seed_sequence])[0]
        
        # Pad the encoding to reach length of the input format of the model
        encoded = pad_sequences([encoded], maxlen = sequence_length, truncating = "pre")
        
        # Using the encoded seed sequence that has been padded, predict the most likely next word
        y_predicted = model.predict_classes(encoded)
        
        # Initialize empty string (required to make the next loop work)
        predicted_word = ""
        
        # For each word, and its index (ID) in the dictionary of words and their ID from the trained tokenizer,
        for word, index, in tokenizer.word_index.items():
            
            # If the index of the newly predicted word matches, assign the word string to "predicted_word"
            if index == y_predicted:
                predicted_word = word
                break
            
        # The seed_sequence should then have added the newly predicted word, with a space in between the words for next runthrough of loop
        seed_sequence = seed_sequence + " " + predicted_word
            
        # The generated string tokens should then be appended to the empty list
        generated_text.append(predicted_word)

    # Join together the tokens in the generated text, to have one coherent string
    generated_string = " ".join(generated_text)
    
    # Return generated string
    return generated_string

def generate_sequences_multiple(model, ngenerate, length, tokenizer, seed_sequences):
    '''
    Function which utilizes the generate_sequences function to generate multiple sequences of a given length using a with a random seed sequence
    
    model: Trained model used to generate new tokens
    ngenerate: Number of new sequences that is wanted to be generated
    length: Desired length of new sequences
    tokenizer: Fitted tokenizer with token ID's
    seed_sequences: A list of sequences that may be used as seeds
    '''
    
    # Empty list of generated strings for appending to
    generated_strings = []

    # Create ngenerate (an integer) generated sequences of text
    for _ in range(0, ngenerate):

        # Take a single random sample from the possible seed sequences and join the tokens to one string
        seed_sequence = " ".join(sample(seed_sequences, 1))

        # Generate a new string, using the seed_sequence as input
        generated_string = generate_sequences(model = model,
                                          tokenizer = tokenizer,
                                          sequence_length = len(seed_sequence),
                                          seed_sequence = seed_sequence,
                                          generated_sequence_length = length)

        # Add newly generated string to list of generated strings
        generated_strings.append(generated_string)
        
    # Return generated_strings
    return generated_strings

'''
###############################################################
---------- Defining the main function of the script -----------
###############################################################
'''
def main(inpath, lstmlayers, batchsize, epochs, ngenerate):
    '''
    Main function of the script.
    
    inpath: Path to the Grimms corpus
    lstmlayers: Number and size of the LSTM layers as a list of integers e.g. [128, 64]
    batchsize: Batchsize for the training
    epochs: Number of epochs to train with
    ngenerate: Number of wanted new generated sequences
    '''
    # Load in the dataset
    df = pd.read_csv(inpath)

    # Create a list of all the texts in the corpus and split it into individual tokens
    text = ' '.join(list(df["Text"])).split()

    # Process the text and return the list of processed tokens.
    tokens = text_processing(text)

    # Get sequences using a running window.
    # E.g. going from ["once upon a time in hollywood"] to ["once upon a", "upon a time", "a time in", "time in hollywood"]
    sequences = get_sequences_running_window(tokens, 51, 1)

    # Vectorize the sequences
    sequences_int, tokenizer = vectorize_sequences(sequences)

    # Assign X (our training variable) all the tokens in each the sequences, except for the last token in the sequence
    X = sequences_int[:, :-1]

    # Assign y (our testing varible) the last token in each of the sequences
    y = sequences_int[:, -1]

    # Define how many unique words we're dealing with
    vocabulary_length = len(set(tokens)) + 1 # +1 for the reserved index

    # Define the length of the training sequences
    sequence_length = X.shape[1]

    # Convert y to one-hot encoding instead of integer.
    y = to_categorical(y, num_classes = vocabulary_length)

    # Initiate model
    model = model_init(vocabulary_length, sequence_length, lstmlayers)
    
    # Fit the model to the data
    print("[INFO] Training the model (this may take a while) ...")
    history = model.fit(X, y, batch_size = batchsize, epochs = epochs)
    
    # Generate new sequences
    print(f"[INFO] Model has been trained. Now generating {ngenerate} new sequences of length 10, 50 and 200 ...")
    
    # Generate "ngenerate" sequences of length 10 
    generated_sequences_10 = generate_sequences_multiple(model, ngenerate, 10, tokenizer, sequences)
    
    # Generate "ngenerate" sequences of length 50
    generated_sequences_30 = generate_sequences_multiple(model, ngenerate, 50, tokenizer, sequences)

    # Have the new sequences as dataframe
    df_seq = pd.DataFrame.from_dict({"length_10" : generated_sequences_10, 
                                     "length_50" : generated_sequences_30})

    # Saving output to out directory
    # Create out folder for the output
    if not os.path.exists("out"): # If the folder does not already exist, create it
        os.makedirs("out")
    
    # Save the training history
    outpath_training_hist = os.path.join("out", "training_hist.png")
    plot_history(history, epochs, outpath_training_hist)
    print(f"[INFO] A plot of the training history has been saved successfully: \"{outpath_training_hist}\"")
        
    # Saving the generated sequences
    outpath_df = os.path.join("out", "generated_sequences.csv")
    df_seq.to_csv(outpath_df)
    print(f"[INFO] A dataframe containing the generated sequences has been saved successfully: \"{outpath_df}\"")
    
'''
###############################################################
----------- Defining use when called from terminal ------------
###############################################################
'''
if __name__=="__main__":
    # Initialise ArgumentParser class
    parser = argparse.ArgumentParser(description = "[SCRIPT DESCRIPTION] Trains a recurrent neural network using LTSM on the Grimms fairy tales. Generates new text sequences in line with the original fairytales")
    
    # Add inpath argument
    parser.add_argument(
        "-i",
        "--inpath", 
        type = str,
        default = os.path.join("data", "grimms_fairytales.csv"),
        required = False,
        help = "str - specifying inpath to the Grimms fairytales")
    
    # Add argument for LTSM layers:
    parser.add_argument(
        "-l",
        "--ltsmlayers", 
        type = int,
        nargs='+', # Allow for multiple integers
        default = [128, 100], # Default LTSM layer structure
        required = False,
        help = "list of integers - specifying number and depth of LTSM layers. e.g. --ltsmlayers 32, 64, 32")
    
    # Add batchsize argument:
    parser.add_argument(
        "-b",
        "--batchsize", 
        type = int,
        default = 64,
        required = False,
        help = "int - specifying batch size for the model training")
    
    # Add epoch argument:
    parser.add_argument(
        "-e",
        "--epochs", 
        type = int,
        default = 350,
        required = False,
        help = "int - specifying number of epochs for the training")

    # Add argument for number of generated sequences:
    parser.add_argument(
        "-n",
        "--ngenerate", 
        type = int,
        default = 50,
        required = False,
        help = "int - specifying how many sequences the script should generate")
    
    # Taking all the arguments we added to the parser and input into "args"
    args = parser.parse_args()
    
    # Performing main function
    main(args.inpath, args.ltsmlayers, args.batchsize, args.epochs, args.ngenerate)
