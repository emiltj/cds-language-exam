#!/usr/bin/python

############### Importing libraries ################
from collections import Counter
from itertools import combinations
from tqdm import tqdm
import os
import sys
import argparse
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import spacy
nlp = spacy.load("en_core_web_sm")

############### Defining main function ###############
def main(edgelist, n, save):
    '''
    Main function for the script
    '''
    # Load in the edgelist
    weighted_edgelist = pd.read_csv(edgelist, index_col = 0)

    # Get only the "n" strongest connections
    weighted_edgelist = weighted_edgelist.sort_values(by=['weight'], ascending = False, na_position='last').iloc[0:n,:]

    # Create a graph from the edgelist
    G = nx.from_pandas_edgelist(weighted_edgelist, 'nodeA', 'nodeB', ["weight"])

    # Create plot from graph
    nx.draw_shell(G, with_labels = True, font_weight= 'bold') 

    # Calculate centrality measures
    
    ev = pd.DataFrame(nx.eigenvector_centrality(G).items(), columns=['node', 'eigenvector_centrality'])
    bc = pd.DataFrame(nx.betweenness_centrality(G).items(), columns=['node', 'betweenness_centrality'])
    dg = pd.DataFrame(nx.degree_centrality(G).items(), columns=['node', 'degree_centrality'])

    # Write values into data frame
    ev = ev.merge(bc, on = "node")
    centrality_measures = ev.merge(dg, on = "node")

    # Save plot and df of centrality measures
    if save == True:
        # Info for terminal
        print("[INFO] Saving visualization and .csv on centrality measures ...")
        
        # Save the centrality measures in the folder "output" (and create the folder if it doesn't already exist)
        output_folder = os.path.join("out", "output")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_path = os.path.join(output_folder, "centrality_measures.csv")
        centrality_measures.to_csv(output_path)
        print(f"[INFO] A new file with centrality measures has been created succesfully: \"{output_path}\"")

        # Save the plot in the folder "viz"  (and create the folder if it doesn't already exist)
        viz_folder = os.path.join("out", "viz")
        if not os.path.exists(viz_folder):
            os.makedirs(viz_folder)
        viz_plot = os.path.join(viz_folder, "network_viz.png")
        plt.savefig(viz_plot, dpi=300, bbox_inches="tight")

        print(f"[INFO] A new visualization has been created succesfully: \"{viz_plot}\"") 

############### Defining use when called from terminal ################
if __name__=="__main__":
    # Initialize parser
    parser = argparse.ArgumentParser(
        description = "[SCRIPT DESCRIPTION] Generates visualization of network as well as calculates centrality measures for nodes of top N weighted pairs.") 

    # Adding argument for inpath for edgelist
    parser.add_argument(
        "-i",
        "--inpath", 
        type = str,
        default = os.path.join("out","weighted_edgelist.csv"), # Default when not specifying a path
        required = False, # Since we have a default value, it is not required to specify this argument
        help = "str containing path to edgelist file")

    # Adding argument for number of top pairs wanted for the network analysis
    parser.add_argument(
        "-n",
        "--n", 
        type = int,
        default = 15, # Default when not specifying anything in the terminal
        required = False, # Since we have a default value, it is not required to specify this argument
        help = "int specifying number of node + edge pairs wanted in the analysis (top n weighted pairs)")
    args = parser.parse_args()

    # Adding argument specifying whether to save or not
    parser.add_argument(
        "-s",
        "--save", 
        type = bool,
        default = True, # Default when not specifying 
        required = False, # Since we have a default value, it is not required to specify this argument
        help = "bool specifying whether to save visualization and centrality measures")

    # Taking all the arguments we added to the parser and input into "args"
    args = parser.parse_args()

    # Executing main function
    main(args.inpath, args.n, args.save)