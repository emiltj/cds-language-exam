#!/usr/bin/python

'''
###############################################################
--------------- Import of modules and libraries ---------------
###############################################################
'''
import os
import sys
import argparse
import pandas as pd
from collections import Counter
from itertools import combinations 
from tqdm import tqdm
import spacy
nlp = spacy.load("en_core_web_sm")
import networkx as nx
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,20)


'''
###############################################################
------------ Defining functions to be used in main ------------
###############################################################
'''
def extract_people_entities(text):
    '''
    From string, extract and return all text entities that have the label "PERSON".
    
    text: A string to extract entities from
    '''
    # Create temporary list 
    text_entities = []
    
    # Get doc object for each of the headlines
    doc = nlp(text)
    
    # For every named entity, append to the temporary list, if the label is "PERSON".
    for entity in doc.ents:
        
        # If label for entity is "PERSON"
        if entity.label_ == "PERSON":
            
            # Append the text to this headlines entity list
            text_entities.append(entity.text)
            
    # Return text_entities
    return text_entities

def create_edgelist(texts_entities):
    '''
    Function that takes a list of text entities and returns an edgelist of all pairs.
    
    Text_entities: A list of lists, with the nested lists containing entities for a given text
    '''
    # Empty list for appending to
    edgelist = []
    
    # Info for terminal use
    print(f"[INFO] Computing edgelist ...")

    # For the each entity list in texts_entities 
    for text_entities in texts_entities:

        # Create an edgelist - i.e. a list of all the pairs of entities.
        edges = list(combinations(text_entities, 2))

        # For each combination (each pair of nodes) append it to the edgelist as a tuple
        for edge in edges:

            # Append to edgelist
            edgelist.append(tuple(sorted(edge)))
    
    # Return the edgelist
    return edgelist


'''
###############################################################
---------- Defining the main function of the script -----------
###############################################################
'''
def main(inpath):
    ''' 
    Main function of the script.
    
    inpath: Path to the news data
    '''
    
    # Read data
    texts = pd.read_csv(inpath)
    
    #texts = texts.sample(10)

    # Subset to not include "fake" and only keep text column
    texts = texts[texts["label"] == "REAL"]["text"]

    # Empty list for appending to
    texts_entities = []

    # Info for terminal use
    print(f"[INFO] Extracting entities from text ...")
    
    # For each of the texts in texts, extract a list of people entities and append to texts_entities
    for text in texts:
        
        # Append the entities from each individual text to list
        texts_entities.append(extract_people_entities(text))

    # Create an edgelist (this one contains duplicates a lot of duplicates, if there are pairs that exist in multiple articles)
    edgelist = create_edgelist(texts_entities)

    # Empty list for appending to
    counted_edges = []

    # For each key and value pair in the dict
    for key, value in Counter(edgelist).items():
        
        # Define source as the first item in key, and target as second.
        source = key[0]
        target = key[1]
        
        # Define weight as the "value" (how many times it is repeated)
        weight = value
        
        # Append to list
        counted_edges.append((source, target, weight))

    # Create a dataframe which contains the edgelist, with "weight" according to how many times the pairs appeared in the different articles 
    edges_df = pd.DataFrame(counted_edges, columns = ["nodeA", "nodeB", "weight"])

    # Define outpath and save dataframe
    if not os.path.exists("out"): # If the folder does not already exist, create it
        os.makedirs("out")
    
    # Define putpath
    outpath = os.path.join("out", "weighted_edgelist.csv")
    
    # Save .csv
    edges_df.to_csv(outpath, sep=",", encoding='utf-8', header = True)
    print(f"A new file has been created \"{outpath}\"")


'''
###############################################################
----------- Defining use when called from terminal ------------
###############################################################
'''
if __name__=="__main__":
    # Define parser
    parser = argparse.ArgumentParser(
        description = "[SCRIPT DESCRIPTION] Generates edgelist from input file")
    
    # Add inputfile argument
    parser.add_argument(
        '-i',
        '--inpath',
        type = str, 
        default = os.path.join("data", "fake_or_real_news.csv"), # Default when not specifying a path
        required = False,
        help = "Inputpath for generating edgelist")

    # Defining "args" from  parser
    args = parser.parse_args()

    # Execute main function
    main(args.inpath)
