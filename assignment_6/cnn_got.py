#!/usr/bin/python

'''
###############################################################
--------------- Import of modules and libraries ---------------
###############################################################
'''
# system tools
import os, sys, argparse
sys.path.append(os.path.join(".."))

# pandas, numpy, gensim
import pandas as pd
import numpy as np
import gensim.downloader
from heapq import nlargest
from scipy import stats

# import my classifier utility functions - see the Github repo!
import utils.classifier_utils as clf

# Machine learning stuff
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import ShuffleSplit
from sklearn.preprocessing import LabelEncoder, LabelBinarizer
from sklearn.metrics import classification_report, confusion_matrix

# tools from tensorflow
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.regularizers import L2
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (Dense, Embedding, 
                                     Flatten, GlobalMaxPool1D, Conv1D)
from tensorflow.keras.optimizers import SGD, Adam

# matplotlib
import matplotlib.pyplot as plt

'''
###############################################################
------------ Defining functions to be used in main ------------
###############################################################
'''
def tokenize_X(X_train, X_test, num_words):
    '''
    Function that tokenizes X_train and X_test. 
    E.g. going from "She's your new queen too." to [172, 8, 275, 103, 129] - each word now has an index pointing to a vocabulary list.
    
    X_train: Features from the training set (words)
    X_test: Features from the test set (words)
    num_words: Number of words to include
    '''
    
    # Initialize tokenizer, using num_words as number of words
    tokenizer = Tokenizer(num_words = num_words)
    
    # Fit tokenizer to training data
    tokenizer.fit_on_texts(X_train)
    
    # Make tokens into sequences
    X_train_tokens = tokenizer.texts_to_sequences(X_train)
    X_test_tokens = tokenizer.texts_to_sequences(X_test)
    
    # Return the sequenized tokens
    return X_train_tokens, X_test_tokens, tokenizer

def apply_padding(X_train, X_test, maxlen, placement):
    '''
    Function that applies padding to X_train and X_test.
    
    X_train: Features for the training set
    X_test: Features for the test set
    maxlen: Length of longest feature set in X_train
    placement: Whether to pad prior or posterior to the text
    '''
    # Apply padding to train
    X_train_pad = pad_sequences(X_train, 
                            padding = placement, # sequences can be padded "pre" or "post"
                            maxlen = maxlen)

    # Apply padding to test
    X_test_pad = pad_sequences(X_test, 
                           padding = placement, 
                           maxlen = maxlen)
    
    # Return padded elements
    return X_train_pad, X_test_pad

def create_embedding_matrix(filepath, word_index, embeddingdim):
    """ 
    A helper function to read in saved GloVe embeddings and create an embedding matrix.
    Courtesy of Ross
    
    filepath: path to GloVe embedding
    word_index: indices from keras Tokenizer
    embeddingedim: dimensions of keras embedding layer
    """
    vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
    embedding_matrix = np.zeros((vocab_size, embeddingdim))

    with open(filepath) as f:
        for line in f:
            word, *vector = line.split()
            if word in word_index:
                idx = word_index[word] 
                embedding_matrix[idx] = np.array(
                    vector, dtype=np.float32)[:embeddingdim]

    return embedding_matrix

def plot_history(H, epoch, outpath):
    """
    Utility function for plotting model history using matplotlib
    Courtesy of Ross (with a minor change)
    
    
    H: model history 
    epochs: number of epochs for which the model was trained
    outpath: Outpath to save the training history plot to
    """
    plt.style.use("fivethirtyeight")
    plt.figure()
    plt.plot(np.arange(0, epoch), H.history["loss"], label="train_loss")
    plt.plot(np.arange(0, epoch), H.history["val_loss"], label="val_loss")
    plt.plot(np.arange(0, epoch), H.history["accuracy"], label="train_acc")
    plt.plot(np.arange(0, epoch), H.history["val_accuracy"], label="val_acc")
    plt.title("Training Loss and Accuracy")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.savefig(outpath, format='png', dpi=100)


'''
###############################################################
---------- Defining the main function of the script -----------
###############################################################
'''
def main(inpath, epoch, batchsize, glovedim, embeddingdim):
    '''
    Main function of the script.
    
    inpath: Path to the Game of Thrones script .csv
    epoch: Number of epochs for training
    batchsize: Batchsize
    glovedim: Which glove to use - number of dimensions
    embeddingdim: Dimensionality for the embedding
    '''
    # Load in the data:
    script = pd.read_csv(inpath)

    # Splitting into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(script['Sentence'].values, # "Features" (sentences)
                                                        script['Season'].values, # Labels
                                                        test_size = 0.15, 
                                                        random_state = 42,
                                                        stratify = script['Season'].values) # If full dataset has 12% sentences from season 1, have 12% of sentences in train + test

    # Tokenize X_train and X_test (i.e. going from "She's your new queen too." to [172, 8, 275, 103, 129]
    # Each word now has an index pointing to a vocabulary list.
    X_train_tokens, X_test_tokens, tokenizer = tokenize_X(X_train, X_test, 10000)

    # Find lenght of longest quote in train
    maxlen = max([len(elem) for elem in X_train]) # Maxlength to be longest element in X_train

    # Apply padding to X_train and X_test
    X_train, X_test = apply_padding(X_train_tokens, X_test_tokens, maxlen, "post")

    # Get labelnames before we binarize labels
    labelnames = sorted(set(y_train))

    # Binarize labels
    lb = LabelBinarizer()
    y_train_encoded = lb.fit_transform(y_train)
    y_test_encoded = lb.fit_transform(y_test)

    # Defining overall vocabulary size (adding 1 because of reserved 0 index)
    vocab_size = len(tokenizer.word_index) + 1 

    # Create an embedding matrix, from glove (depending on argument)
    if glovedim == 50:
        glove = "glove.6B.50d.txt"
    elif glovedim == 100:
        glove = "glove.6B.100d.txt"

    # Creating an embedding matrix
    embedding_matrix = create_embedding_matrix(os.path.join("data", "glove", glove),
                                               tokenizer.word_index, 
                                               embeddingdim)

    # Define model type, optimizer, layers and compile model
    model = Sequential() # Initialize sequential model
    opt = tf.keras.optimizers.Adam(learning_rate = 0.01) # Define optimizer
    # Add embedding layer
    model.add(Embedding(input_dim = vocab_size, # Vocabulary size (from Tokenizer())
                        output_dim = embeddingdim, # Embedding dimensions as defined by argument
                        input_length = maxlen, # Input length should be length of inputs after padding
                        weights = [embedding_matrix], # Weights from the embedding matrix
                        trainable = True)) # The model may train on the embeddings

    # CONV+ReLU -> MaxPool -> FC+ReLU -> Out
    model.add(Conv1D(8, 3, activation='relu'))
    model.add(GlobalMaxPool1D())
    model.add(Dense(16, kernel_regularizer = L2(0.1), activation = 'relu'))
    model.add(Dense(8,  activation = 'softmax')) # Multiclass classification needs softmax in the final activation layer
    model.compile(loss = 'categorical_crossentropy', optimizer = opt, metrics = ['accuracy']) # Compile model (loss categorical - multiple classes)

    # Train model
    print(f"[INFO] Training CNN classifier ...")
    history = model.fit(X_train, y_train_encoded,
                        epochs = epoch,
                        verbose = True,
                        validation_data = (X_test, y_test_encoded),
                        batch_size = batchsize)

    # Print accuracy/loss over epochs (and save)
    outpath = os.path.join("out", 'cnn_training_history.png')
    plot_history(history, epoch, outpath)
    print(f"[INFO] A plot of the training history has been saved succesfully: \"{outpath}\"")

    # Get predictions:
    predictions = model.predict(X_test)
    
    # Evaluation (classification report and confusion matrix)
    # Get classification report from predictions
    classif_report = pd.DataFrame(classification_report(y_test_encoded.argmax(axis = 1),
                                    predictions.argmax(axis = 1),
                                    target_names = labelnames, 
                                    zero_division = 0,
                                    output_dict = True))
    
    # Get confusion matrix
    conf_matrix = pd.DataFrame(confusion_matrix(y_test_encoded.argmax(axis = 1),
                                    predictions.argmax(axis = 1)))
    
    # Print performance to terminal
    print(f"[PERFORMANCE INFO] Classification report:") # Info to terminal
    print(classif_report)
    print(f"[PERFORMANCE INFO] Confusion matrix (rows refer to True class, while columns refer to Predicted class):") # Info to terminal
    print(conf_matrix)
    
    # Save performance in "out"
    # If the folder does not already exist, create it
    if not os.path.exists("out"):
        os.makedirs("out")

    # Define outpath
    classif_outpath = os.path.join("out", "cnn_classif_report.csv")
    conf_outpath = os.path.join("out", "cnn_conf_matrix.csv")
    
    # Save (and print info to terminal)
    classif_report.to_csv(classif_outpath)
    print(f"[INFO] Classification report has been saved succesfully: \"{classif_outpath}\"")
    conf_matrix.to_csv(conf_outpath)
    print(f"[INFO] Confusion matrix has been saved succesfully: \"{conf_outpath}\"")
    
    # Print overview of potential overfitting of the model
    loss, accuracy = model.evaluate(X_train, y_train_encoded, verbose = False)
    print("[PERFORMANCE INFO] Training Accuracy: {:.4f}".format(accuracy))
    loss, accuracy = model.evaluate(X_test, y_test_encoded, verbose = False)
    print("[PERFORMANCE INFO] Testing Accuracy:  {:.4f}".format(accuracy))
    
'''
###############################################################
----------- Defining use when called from terminal ------------
###############################################################
'''
if __name__=="__main__":
    # Initialise ArgumentParser class
    parser = argparse.ArgumentParser(description = "[SCRIPT DESCRIPTION] Script that trains a convolutional neural networks classifier to predict season from dialogue")
    
    # Add inpath argument
    parser.add_argument(
        "-i",
        "--inpath", 
        type = str,
        default = os.path.join("data", "Game_of_Thrones_Script.csv"),
        required = False,
        help= "str - specifying inpath to Game of Thrones script")
    
    # Add epoch argument
    parser.add_argument(
        "-e",
        "--epoch", 
        type = int,
        default = 10,
        required = False,
        help= "int - specifying number of epochs for the cnn model training")
    
    # Add batch size argument
    parser.add_argument(
        "-b",
        "--batchsize",
        type = int, 
        default = 100,
        required = False,
        help = "int - specifying batch size")
    
    # Add glove dimensions argument
    parser.add_argument(
        "-g",
        "--glovedim", 
        type = int,
        default = 50,
        required = False,
        help= "int - specifying which how many dimensions should be in the glove embedding to use. Options: 50 or 100")

    # Add embedding dimension argument
    parser.add_argument(
        "-E",
        "--embeddingdim", 
        type = int,
        default = 50,
        required = False,
        help= "int - specifying dimensions for the embedding")
    
    # Taking all the arguments we added to the parser and input into "args"
    args = parser.parse_args()
    
    # Performing main function
    main(args.inpath, args.epoch, args.batchsize, args.glovedim, args.embeddingdim)
