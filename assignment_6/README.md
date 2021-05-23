<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/emiltj/cds-language-exam">
    <img src="../README_images/lang_logo.png" alt="Logo" width="100" height="100">
  </a>
  
  <h2 align="center">Text classification using Deep Learning</h2>

  <p align="center">
    Assignment 6
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
_Winter is... hopefully over._

In class this week, we've seen how deep learning models like CNNs can be used for text classification purposes. For your assignment this week, I want you to see how successfully you can use these kind of models to classify a specific kind of cultural data - scripts from the TV series Game of Thrones.

You can find the data [here](https://www.kaggle.com/albenft/game-of-thrones-script-all-seasons)

In particular, I want you to see how accurately you can model the relationship between each season and the lines spoken. That is to say - can you predict which season a line comes from? Or to phrase that another way, is dialogue a good predictor of season?
* Start by making a baseline using a 'classical' ML solution such as CountVectorization + LogisticRegression and use this as a means of evaluating how well your model performs.
* Then you should try to come up with a solution which uses a DL model, such as the CNNs we went over in class.

<!-- METHODS -->
## Methods

**Specifically for this assignment:**

For the Logistic Regression (LR) classification task, I start by loading in the data. I then do a stratified train-test split of the data, as the data set is unbalanced. Stratification locks the distribution of classes in the train and test sets - i.e. if season 1 entries account for 23% of the entire dataset, then both the train and test set will consist of 23% data from season 1. The dialogue is then vectorized. The sentences are converted to vectors as CNN's only take vectors as input. Each number in the vectors represent a word index in a vocabulary list (which contains the feature names). The feature vectors and the labels from the training data are then used to train the LR classifer, a model which is subsequently tested on the test split. A classification matrix is saved, a long with a confusion matrix to the folder ```out``` .

For the Convolutional Neural Networks (CNN) classification task, the data is split up into a train-test split using stratification.



**On a more general level (this applies to all assignments):**

I have tried to as accessible and user-friendly as possible. This has been attempted by the use of:

* Smaller functions. These are intended to solve the sub-tasks of the assignment. This is meant to improve readability of the script, as well as simplifying the use of the script.
* Information prints. Information is printed to the terminal to allow the user to know what is being processed in the background
* Argparsing. Arguments that let the user determine the behaviour and paths of the script (see "Optional arguments" section for more information)

<!-- RESULTS AND DISCUSSION -->
## Results and discussion

**Logistic Regression classification:**

|           |                     |                     |                     |                     |                     |                     |                     |                     |                    |                     |                    | 
|-----------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|--------------------|---------------------|--------------------| 
|           | Season 1            | Season 2            | Season 3            | Season 4            | Season 5            | Season 6            | Season 7            | Season 8            | accuracy           | macro avg           | weighted avg       | 
| precision | 0.29 | 0.27 | 0.24 | 0.26 | 0.25  | 0.33 | 0.39  | 0.25 | 0.28 | 0.28 | 0.28 | 
| recall    | 0.31 | 0.37  | 0.26  | 0.29 | 0.24 | 0.24 | 0.29 | 0.09 | 0.28 | 0.26 | 0.28 | 
| f1-score  | 0.30  | 0.31  | 0.25                | 0.27 | 0.25 | 0.28  | 0.33   | 0.13 | 0.28 | 0.27  | 0.27 | 
| support   | 477.0               | 587.0               | 536.0               | 517.0               | 455.0               | 429.0               | 366.0               | 220.0               | 0.28 | 3587.0              | 3587.0             | 



**Convolutional Neural Networks classification:**

|           |                     |                     |                     |                     |                     |                     |                     |                     |                     |                     |                     | 
|-----------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------|---------------------| 
|           | Season 1            | Season 2            | Season 3            | Season 4            | Season 5            | Season 6            | Season 7            | Season 8            | accuracy            | macro avg           | weighted avg        | 
| precision | 0.33 | 0.26 | 0.23 | 0.18  | 0.16 | 0.22 | 0.22 | 0.18 | 0.22 | 0.22 | 0.23 | 
| recall    | 0.34 | 0.27  | 0.14  | 0.36 | 0.13 | 0.08 | 0.32 | 0.09 | 0.22 | 0.21 | 0.22 | 
| f1-score  | 0.33  | 0.26  | 0.17 | 0.24  | 0.14  | 0.12 | 0.26  | 0.12 | 0.22 | 0.21 | 0.21 | 
| support   | 477.0               | 587.0               | 536.0               | 517.0               | 455.0               | 429.0               | 366.0               | 220.0               | 0.22 | 3587.0              | 3587.0              | 




<!-- USAGE -->
## Usage

Make sure to follow the instructions in the README.md located at the parent level of this repository, for the required installation of the virtual environment as well as the data download.

Subsequently, use the following code (when within the ```cds-language-exam``` folder):

```bash
cd assignment_3
source ../lang101/bin/activate # If not already activated
python ___________________________________________________________________.py
```

### Optional arguments:

image_search.py arguments for commandline to consider:
-       "-f"
        "--filepath", 
        type = str,
        default = os.path.join("data", "*.jpg"), # Default path to corpus, when none is specified
        required = False,
        help= "str - path to image corpus")

<!-- CONTACT -->
## Contact

Feel free to write me, Emil Jessen for any questions.
You can do so on [Slack](https://app.slack.com/client/T01908QBS9X/D01A1LFRDE0) or on [Facebook](https://www.facebook.com/emil.t.jessen/).
