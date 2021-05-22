<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/emiltj/cds-language-exam">
    <img src="../README_images/lang_logo.png" alt="Logo" width="100" height="100">
  </a>
  
  <h2 align="center">Sentiment analysis</h2>

  <p align="center">
    Assignment 3
    <br />
    <a href="https://github.com/emiltj/cds-language-exam/issues">Report Bug</a>
    ·
    <a href="https://github.com/emiltj/cds-language-exam/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#assignment-description">Assignment description</a></li>
    <li><a href="#methods">Methods</a></li>
    <li><a href="#results-and-discussion">Results and discussion</a></li>
    <li><a href="#usage">Usage</a></li>
          <ul>
        <li><a href="#optional-arguments">Optional arguments</a></li>
      </ul>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ASSIGNMENT DESCRIPTION -->
## Assignment description

Use the dataset ["A million headlines"](https://www.kaggle.com/therohk/million-headlines) - headlines from the Australian news source ABC (Start Date: 2003-02-19 ; End Date: 2020-12-31).

Do the following:
* Calculate the sentiment score for every headline in the data. You can do this using the spaCyTextBlob approach that we covered in class or any other dictionary-based approach in Python.
* Create and save a plot of sentiment over time with a 1-week rolling average
* Create and save a plot of sentiment over time with a 1-month rolling average
* Make sure that you have clear values on the x-axis and that you include the following: a plot title; labels for the x and y axes; and a legend for the plot
* Write a short summary (no more than a paragraph) describing what the two plots show. You should mention the following points: 1) What (if any) are the general trends? 2) What (if any) inferences might you draw from them?

<!-- METHODS -->
## Methods

**Specifically for this assignment:**

The script first converts the dates to datetime format and then calculates the sentiment scores for each of the headlines. To calculate sentiment scores, I use the SpaCy model [en_core_web_sm](https://spacy.io/usage/models). After calculating the sentiment scores the average for each day is then computed. The smoothed scores are subsequently computed using moving windows of window sizes 7 and 30 (weekly and monthly smoothing). For creating the plots, I used matplotlib to have all 4 subplots in a single plot to provide a clear overview.

**On a more general level (this applies to all assignments):**

I have tried to as accessible and user-friendly as possible. This has been attempted by the use of:
* Smaller functions. These are intended to solve the sub-tasks of the assignment. This is meant to improve readability of the script, as well as simplifying the use of the script.
* Information prints. Information is printed to the terminal to allow the user to know what is being processed in the background
* Argparsing. Arguments that let the user determine the behaviour and paths of the script (see <a href="#optional-arguments">"Optional arguments"</a> section for more information)

<!-- RESULTS AND DISCUSSION -->
## Results and discussion

<p align="center"><a href="https://github.com/emiltj/cds-language-exam/blob/main/assignment_3/out/daily_sentiment_scores.png"><img src="./out/daily_sentiment_scores.png" alt="Logo" width="240" height="150"></a></p>
<p align="center"><em>Sentiment scores over time, no smoothing</em><p/>

<p align="center"><a href="https://github.com/emiltj/cds-language-exam/blob/main/assignment_3/out/daily_sentiment_scores_weekly_smooth.png""><img src="./out/daily_sentiment_scores_weekly_smooth.png" alt="Logo" width="240" height="150"></a>   <a href="https://github.com/emiltj/cds-language-exam/blob/main/assignment_3/out/daily_sentiment_scores_monthly_smooth.png"><img src="./out/daily_sentiment_scores_monthly_smooth.png" alt="Logo" width="240" height="150"></a></p>
<p align="center"><em>Sentiment scores over time, 7-day smoothing &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Sentiment scores over time, 30-day smoothing</em><p/>



The plot quite clearly depicts a pattern of great fluctuation on a daily basis. However, when smoothing the sentiment scores more general trends become visible - especially when using a 7-day rolling mean smoothing. 
One of these trends is an especially positive trend around the dates 15th of March to the 22 of March, 2003.
It is hard to make any inferences as to what might have caused this spike in positivity around that date.

<!-- USAGE -->
## Usage

Make sure to follow the instructions in the README.md located at the parent level of this repository, for the required installation of the virtual environment as well as the data download.

Subsequently, use the following code (when within the ```cds-language-exam``` folder):

```bash
cd assignment_3
source ../lang101/bin/activate # If not already activated
python sentiment.py
```

### Optional arguments:

image_search.py arguments for commandline to consider:
-       '-i',
        '--inputpath',
        type = str,
        default = os.path.join("data", "abcnews-date-text.csv"),
        required = False,
        help = f"str - path to .csv. n")
-       '-t',
        '--test',
        type = bool,
        default = False,
        required = False,
        help = 'bool - if True, then performs only on a subset. False is on the full dataset')

<!-- CONTACT -->
## Contact

Feel free to write me, Emil Jessen for any questions.
You can do so on [Slack](https://app.slack.com/client/T01908QBS9X/D01A1LFRDE0) or on [Facebook](https://www.facebook.com/emil.t.jessen/).
