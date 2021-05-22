#!/usr/bin/python

############### Importing libraries ################
import os, re, datetime, glob, spacy, argparse, spacy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from spacytextblob.spacytextblob import SpacyTextBlob
nlp = spacy.load("en_core_web_sm")
spacy_text_blob = SpacyTextBlob()

############### Defining functions to be used in main ###############
def convert_to_datetime(date_col):
    '''
    Function which converts a column to datetime.
    
    date_col: A date column (pd.Series)
    '''
    # Info for terminal use
    print("[INFO] Converting date column to datetime format ...")
    
    # Creating an empty list which is going to contain the dates in date format instead of numerical
    dates = []
    
    # For every item in date_col, append it in datetime format to "dates" list
    for i in list(date_col):
        date = str(i) # take date and convert to string
        date = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:])) # use datetime.date to make the date into datetime, using indices
        dates.append(date) # append to "dates" list

    # Return the data in datetime format
    return dates

# Calculate sentiment scores for each headline
def calc_sentiment(text_col):
    '''
    Function that calculates sentiment scores for a column of strings.
    
    text_col: A column strings (pd.Series)
    '''
    # Info for terminal use
    print("[INFO] Calculating sentiment scores ...")

    # Calculate sentiment for all headlines and add the sentiment score to the dataframe
    sentiment_score = []
    for doc in nlp.pipe(list(text_col)):
        score = doc._.sentiment.polarity
        sentiment_score.append(score)
        
    # Return the sentiment score
    return sentiment_score

# Calculate daily average sentiment scores. Also smoothed scores
def calc_daily_avg_sentiment(date_col, sentiment_score_col):
    '''
    Function that calculates daily average sentiment scores from date column and sentiment score column. 
    Returns a data frame with average scores and average scores smoothed over a weekly and a monthly basis.
    
    date_col: Column with dates in date() format (pd.Series)
    sentiment_score_col: Column with sentiment scores for all entries (pd.Series)
    '''
    # Info for terminal use
    print("[INFO] Calculating mean daily sentiment scores (this may take while) ...")

    # Get a list of all unique dates
    unique_dates = list(date_col.unique())

    # Create empty list, which is to contain the mean sentiment score for a given unique date
    daily_mean_sentiment_score = []

    # Merge lists into dataframe
    dff = pd.DataFrame({'date_col': date_col, 'sentiment_score_col': sentiment_score_col})

    # For each unique date get the mean of all sentiment scores and store it in "daily_mean_sentiment_score"
    for unique_date in unique_dates:
        df_for_date_n = dff.loc[dff["date_col"] == unique_date]
        mean_for_date_n = np.mean(df_for_date_n["sentiment_score_col"])
        daily_mean_sentiment_score.append(mean_for_date_n)

    # Convert to series object
    daily_mean_sentiment_score = pd.Series(daily_mean_sentiment_score)

    # Calculate smoothed mean scores for each date, using a window of 7 and 30 days
    daily_sentiment_score_weekly_smooth = daily_mean_sentiment_score.rolling(7).mean() # 7 days
    daily_sentiment_score_monthly_smooth = daily_mean_sentiment_score.rolling(30).mean() # 30 days

    # Create a new df, with daily sentiment scores
    df_daily = pd.DataFrame({
        'date' : unique_dates,
        'sentiment_score' : daily_mean_sentiment_score,
        'sentiment_score_weekly_smooth' : daily_sentiment_score_weekly_smooth,
        'sentiment_score_monthly_smooth' : daily_sentiment_score_monthly_smooth})

    # Return df
    return df_daily

# Plotting the scores
def plot_sentiment(df, outname):
    '''
    Function that plots sentiment scores.
    
    df: Dataframe containing raw sentiment scores, and sentiment scores smoothed daily and weekly. Also has to contain a date column.
    outname: Name of file to be saved
    '''
    # Adding a figure which is large enough for multiple subplots
    fig = plt.figure(figsize = (42.0, 8.0))

    # Adding subplots
    axes_1 = fig.add_subplot(1,4,1) # 1 row, 3 columns, 2nd position
    axes_2 = fig.add_subplot(1,4,2) # 1 row, 3 columns, 4th position 
    axes_3 = fig.add_subplot(1,4,3) # 1 row, 3 columns, 5th position
    axes_4 = fig.add_subplot(1,4,4) # 1 row, 3 columns, 6th position

    # Defining axes_1 plot
    axes_1.plot(df["date"], df["sentiment_score"], "b", linewidth = 2)
    axes_1.plot(df["date"], df["sentiment_score_weekly_smooth"], "g", linewidth = 2)
    axes_1.plot(df["date"], df["sentiment_score_monthly_smooth"], "r", linewidth = 2)
    axes_1.set_title("Mean sentiment score of headlines")
    axes_1.set_xlabel("Dates")
    axes_1.set_ylabel("Mean sentiment scores")
    axes_1.legend(["Daily sentiment", "Daily sentiment, smoothed 7-days", "Daily sentiment, smoothed 30-days"])
    axes_1.xaxis_date() # Tell matplotlib to interpret the x-axis values as dates
    
    # Defining axes_2 plot
    axes_2.set_title("Mean sentiment score of headlines")
    axes_2.set_ylabel("Mean sentiment score")
    axes_2.set_xlabel("Dates")
    axes_2.plot(df["date"], df["sentiment_score"], "b", linewidth = 2)
    axes_2.xaxis_date() # Tell matplotlib to interpret the x-axis values as dates

    # Defining axes_3 plot
    axes_3.set_title("Mean sentiment score of headlines \n (smoothed, 7-day window)")
    axes_3.set_ylabel("Mean sentiment score (smoothed, 7-days)")
    axes_3.set_xlabel("Dates")
    axes_3.plot(df["date"], df["sentiment_score_weekly_smooth"], "g", linewidth = 2)
    axes_3.xaxis_date() # Tell matplotlib to interpret the x-axis values as dates

    # Defining axes_4 plot
    axes_4.set_title("Mean sentiment score of headlines \n (smoothed, 30-day window)")
    axes_4.set_ylabel("Mean sentiment score (smoothed, 30-days)")
    axes_4.set_xlabel("Dates")
    axes_4.plot(df["date"], df["sentiment_score_monthly_smooth"], "r", linewidth = 2)
    axes_4.xaxis_date() # Tell matplotlib to interpret the x-axis values as dates

    plt.tight_layout() # So that the font doesn't overlap
    fig.autofmt_xdate() # Tilt x-axis labels, to make room for them
    
    # Saving the plot
    # If the folder does not already exist, create it
    if not os.path.exists("out"):
        os.makedirs("out")
    
    # Create outpath for plot and save
    outpath = os.path.join("out", outname)
    plt.savefig(outpath)
    print(f"[INFO] A sentiment_polarity plot has been saved succesfully: \"{outpath}\"")

############### Defining main function ###############
def main(inputpath, test):
    '''
    Main function.
    
    inputpath: Path to news document
    test: Bool, specifying whether to run a test of the script on only a subset of the data (to allow for faster processing)
    '''
    # Read csv for inputpath
    df = pd.read_csv(inputpath)
    
    # If test == true, only do a subset of the full dataset
    if test == True:
        df = df.iloc[:10000, : ]
        
    # Convert publish_date to datetime format
    df["publish_date"] = convert_to_datetime(df["publish_date"])
    
    # Calculate sentiment score and create a new column in the df
    df["sentiment_score"] = calc_sentiment(df["headline_text"])
    
    # Calculate daily average sentiment scores as well as the weekly and monthly smoothing
    df_daily = calc_daily_avg_sentiment(date_col = df["publish_date"], sentiment_score_col = df["sentiment_score"])
    
    # Save plot of the sentiment scores over time
    plot_sentiment(df_daily, "sentiment_polarity_plot.png")

############### Defining use when called from terminal ################
if __name__=="__main__":
    # Define parser
    parser = argparse.ArgumentParser(description='[SCRIPT DESCRIPTION] A script that computes sentiment scores for headlines and averages sentiment scores of headlines within dates. Furthermore smoothes this average over a window of 7 and 30 days, respectively - as well as plots the average sentiment scores for each day.')

    # Add inpath argument
    parser.add_argument(
    '-i',
    '--inputpath',
    type = str,
    default = os.path.join("data", "abcnews-date-text.csv"),
    required = False,
    help = f"str - path to .csv. n")

    # Add test argument
    parser.add_argument(
    '-t',
    '--test',
    type = bool,
    default = False,
    required = False,
    help = 'bool - if True, then performs only on a subset. False is on the full dataset')

    # Taking all the arguments we added to the parser and input into "args"
    args = parser.parse_args()

    # Perform main function
    main(args.inputpath, args.test)