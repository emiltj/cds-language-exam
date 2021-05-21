#!/usr/bin/python

############################### Importing libraries ################################
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
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics

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

tf.keras.backend.clear_session()

############################### Defining functions to be used in main ###############################
def create_embedding_matrix(filepath, word_index, embedding_dim):
    """ 
    A helper function to read in saved GloVe embeddings and create an embedding matrix
    
    filepath: path to GloVe embedding
    word_index: indices from keras Tokenizer
    embedding_dim: dimensions of keras embedding layer
    """
    vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
    embedding_matrix = np.zeros((vocab_size, embedding_dim))

    with open(filepath) as f:
        for line in f:
            word, *vector = line.split()
            if word in word_index:
                idx = word_index[word] 
                embedding_matrix[idx] = np.array(
                    vector, dtype=np.float32)[:embedding_dim]

    return embedding_matrix

def plot_history(H, epoch):
    """
    Utility function for plotting model history using matplotlib
    
    H: model history 
    epochs: number of epochs for which the model was trained
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
    plt.savefig(os.path.join("out", f'cnn_training_history.png'), format='png', dpi=100)

############### Defining main function ###############
def main(inpath, epoch, batchsize, glove_dim):
    
    # Load in the data:
    script = pd.read_csv(inpath)

    # Splitting into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(script['Sentence'].values, # "Features" (sentences)
                                                        script['Season'].values, # Labels
                                                        test_size = 0.15, 
                                                        random_state = 42,
                                                        stratify = script['Season'].values) # If full dataset has 12% sentences from season 1, have 12% of sentences in train + test

    # CountVectorizer() had a token count array for each sentence
    # Here we simply have an array of numbers, which corresponds to a word's index in the vocabulary (of all words)
    # Tokenize X
    tokenizer = Tokenizer(num_words = 2500) # Num_words = the most common num_words-1
    
    # Fit tokenizer to training data
    tokenizer.fit_on_texts(X_train)
    
    # Make tokens into sequences
    X_train_toks = tokenizer.texts_to_sequences(X_train)
    X_test_toks = tokenizer.texts_to_sequences(X_test)
    
     # Overall vocabulary size (adding 1 because of reserved 0 index)
    vocab_size = len(tokenizer.word_index) + 1 

    # Apply padding
    maxlen = max([len(elem) for elem in X_train_toks]) # Maxlength to be longest element in X_train

    X_train_pad = pad_sequences(X_train_toks, 
                                padding='post', # sequences can be padded "pre" or "post"
                                maxlen=maxlen)

    X_test_pad = pad_sequences(X_test_toks, 
                               padding='post', 
                               maxlen=maxlen)

    # Encode labels from "Season 8" -> "8"
    label_encoder = LabelEncoder()
    y_test_encoded = label_encoder.fit_transform(y_test)
    y_train_encoded = label_encoder.fit_transform(y_train)

    # Load in embedding matrix
    embedding_dim = 50 # define embedding size we want to work with

    # Create an embedding matrix, from glove (depending on argument)
    if glove_dim == 50:
        glove = "glove.6B.50d.txt"
    elif glove_dim == 100:
        glove = "glove.6B.100d.txt"
        
    embedding_matrix = create_embedding_matrix(os.path.join("data", "glove", glove),
                                               tokenizer.word_index, 
                                               embedding_dim)
    
    # Define model
    model = Sequential() # Initialize sequential model

    # Define optimizer
    opt = tf.keras.optimizers.Adam(learning_rate=0.001)

    # add Embedding layer
    model.add(Embedding(input_dim = vocab_size,     # vocab size from Tokenizer()
                        output_dim = embedding_dim, # user defined embedding size
                        input_length = maxlen, # maxlen of padded docs
                        weights = [embedding_matrix],
                        trainable = False)) # Embeddings are static     

    # CONV+ReLU -> MaxPool -> FC+ReLU -> Out
    model.add(Conv1D(8, 3, 
                    activation='relu'))
    model.add(GlobalMaxPool1D())
    model.add(Dense(8, kernel_regularizer=L2(0.1), 
                    activation='relu'))
    model.add(Dense(1, 
                    activation='softmax')) # softmax because multiclass

    # Compile model
    model.compile(loss = 'categorical_crossentropy', # categorical, because multiclass
                  optimizer = opt,
                  metrics = ['accuracy'])

    # Train model
    print(f"[INFO] Commencing training, using {epoch} epochs")
    history = model.fit(X_train_pad, y_train_encoded,
                        epochs = epoch,
                        verbose = True,
                        validation_data = (X_test_pad, y_test_encoded),
                        batch_size = batchsize)

    
    # Show plot of accuracy and loss over epochs and save it
    plot_history(history, epoch)
    print(f"A plot history report has been saved succesfully: \"out/cnn_training_history.png\"")
    
    loss, accuracy = model.evaluate(X_train_pad, y_train_encoded, verbose=False)
    print("Training Accuracy: {:.4f}".format(accuracy))
    loss, accuracy = model.evaluate(X_test_pad, y_test_encoded, verbose=False)
    print("Testing Accuracy:  {:.4f}".format(accuracy))

############################### Defining use when called from terminal ################################
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
    
    # Add inpath argument
    parser.add_argument(
        "-e",
        "--epoch", 
        type = int,
        default = 5,
        required = False,
        help= "int - specifying number of epochs for the cnn model training")
    
    # Add batch size argument
    parser.add_argument(
        "-b",
        "--batchsize",
        type = int, 
        default = 200,
        required = False,
        help = "int - specifying batch size")
    
    # Add inpath argument
    parser.add_argument(
        "-g",
        "--glovedim", 
        type = int,
        default = 50,
        required = False,
        help= "int - specifying which how many dimensions should be in the glove embedding to use. Options: 50 or 100")

    
    # Taking all the arguments we added to the parser and input into "args"
    args = parser.parse_args()
    
    # Performing main function
    main(args.inpath, args.epoch, args.batchsize, args.glovedim)