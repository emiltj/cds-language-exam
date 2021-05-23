#!/usr/bin/python

'''
###############################################################
--------------- Import of modules and libraries ---------------
###############################################################
'''
# system tools
import os, sys, argparse
sys.path.append(os.path.join(".."))
import pandas as pd

# import my classifier utility functions - see the Github repo!
import utils.classifier_utils as clf

# Machine learning stuff
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import ShuffleSplit
from sklearn import metrics

# matplotlib
import matplotlib.pyplot as plt

'''
###############################################################
---------- Defining the main function of the script -----------
###############################################################
'''
def main(inpath):
    '''
    Main function of the script.
    
    inpath: Specifies path to the GoT script
    '''
    # Load in the data:
    script = pd.read_csv(inpath)

    # Splitting into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(script['Sentence'].values, # "Features" (sentences)
                                                        script['Season'].values, # Labels
                                                        test_size = 0.15, 
                                                        random_state = 42,
                                                        stratify = script['Season'].values) # If full dataset has 12% sentences from season 1, have 12% of sentences in train + test

    # Instead of having sentences, get token count vectors
    vectorizer = CountVectorizer()
    X_train_feats = vectorizer.fit_transform(X_train)
    X_test_feats = vectorizer.transform(X_test) 
    feature_names = vectorizer.get_feature_names() # Get feature names (words from the numbers)
    
    # Basic logistic regression, train + predict
    # Define classifer
    classifier = LogisticRegression(random_state = 42, max_iter = 1000) # With max iterations = 1000 to avoid convergence issues.

    # Train the model
    print(f"[INFO] Training logistic regression classifier ...") # Info to terminal
    classifier.fit(X_train_feats, y_train)

    # Test model on validation set
    print(f"[INFO] Testing the logistic regression classifier ...") # Info to terminal
    y_pred = classifier.predict(X_test_feats)

    # Evaluation (classification report and confusion matrix)
    classif_report = pd.DataFrame(metrics.classification_report(y_test, y_pred, output_dict = True))
    conf_matrix = pd.DataFrame(metrics.confusion_matrix(y_test, y_pred))
    
    # Print performance to terminal
    print(f"[PERFORMANCE INFO] Classification report:") # Info to terminal
    print(classif_report)
    print(f"[PERFORMANCE INFO] Confusion matrix (rows refer to True class, while columns refer to Predicted class):") # Info to terminal
    print(conf_matrix)
    
    # Save performance in "out"
    # If the folder "out" does not already exist, create it
    if not os.path.exists("out"):
        os.makedirs("out")
    
    # Define outpath
    classif_outpath = os.path.join("out", "lr_classif_report.csv")
    conf_outpath = os.path.join("out", "lr_conf_matrix.csv")
    
    # Save (and print info to terminal)
    classif_report.to_csv(classif_outpath)
    print(f"[INFO] Classification report has been saved succesfully: \"{classif_outpath}\"")
    conf_matrix.to_csv(conf_outpath)
    print(f"[INFO] Confusion matrix has been saved succesfully: \"{conf_outpath}\"")

'''
###############################################################
----------- Defining use when called from terminal ------------
###############################################################
'''
if __name__=="__main__":
    # Initialise ArgumentParser class
    parser = argparse.ArgumentParser(description = "[SCRIPT DESCRIPTION] Script that trains a logistic regression classifier to predict season from dialogue")
    
    # Add inpath argument
    parser.add_argument(
        "-i",
        "--inpath", 
        type = str,
        default = os.path.join("data", "Game_of_Thrones_Script.csv"),
        required = False,
        help= "str - specifying inpath to Game of Thrones script")
    
    # Taking all the arguments we added to the parser and input into "args"
    args = parser.parse_args()
    
    # Performing main function
    main(args.inpath)
