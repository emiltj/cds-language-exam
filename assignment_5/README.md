<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/emiltj/cds-language-exam">
    <img src="../README_images/lang_logo.png" alt="Logo" width="100" height="100">
  </a>
  
  <h2 align="center">(Un)supervised machine learning - LDA and Topic modeling on philosophical texts</h2>

  <p align="center">
    Assignment 5
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
### General assignment description
_Pick your own dataset to study.
Train an LDA model on your data to extract structured information that can provide insight into your data. For example, maybe you are interested in seeing how different authors cluster together or how concepts change over time in this dataset. You should formulate a short research statement explaining why you have chosen this dataset and what you hope to investigate. This only needs to be a paragraph or two long and should be included as a README file along with the code. E.g.: I chose this dataset because I am interested in... I wanted to see if it was possible to predict X for this corpus. You should also include a couple of paragraphs in the README on the results, so that a reader can make sense of it all. E.g.: I wanted to study if it was possible to predict X. The most successful model I trained had a weighted accuracy of 0.6, implying that it is not possible to predict X from the text content alone. And so on._

_Tips_

* _Think carefully about the kind of preprocessing steps your text data may require - and document these decisions!_
* _Your choice of data will (or should) dictate the task you choose - that is to say, some data are clearly more suited to supervised than unsupervised learning and vice versa. * Make sure you use an appropriate method for the data and for the question you want to answer_
* _Your peer reviewer needs to see how you came to your results - they don't strictly speaking need lots of fancy command line arguments set up using argparse(). You should still try to have well-structured code, of course, but you can focus less on having a fully-featured command line tool_

### My assignment description
This assignment seeks to use Latent Dirichlet Analysis (LDA) as a tool topic modeling tool to investigate philosophical texts in an exploratory manner.
More specifically, I want to investigate whether particular schools of philosophical thought cluster together in terms of topics. To dig a little bit deeper, I also want to do the same type of investigation into the individual books that make up the corpus - in other words not just look at schools as a homogeneous group.

* Merge paragraphs from the same books together in the philosophical text corpus.
* Perform LDA, using bigram and trigram models ensure that the LDA utilizes 5 topics
* Create a visualization that depicts each philosophical schools' respective topic prevalence from all 5 topics.
* Reduce the 5-dimensional space to 2 dimensions using Principal Component Analysis (PCA)
* Plot the individual books in this PCA-space (with X and Y axes showing principal component 1 and 2)
* Plot the individual schools in this PCA-space (with X and Y axes showing principal component 1 and 2)
* Save a document showing the most important words for each of the 5 topics

<!-- METHODS -->
## Methods

**Specifically for this assignment:**

For this assignment, I first aggregated all data from the same book title together as I wanted to look at individual books for my visualizations. I then built bigram and trigram models - contiguous sequences of 2 or 3 items (with items being individual words in this analysis). I then processed the data using these models, only keeping nouns, adjectives, verbs and adverbs. As this kind of analysis only takes vectors, I created a dictionary so I could convert each word in each of the entries into an integer value (with the value functioning like an ID for the dictionary).
Using the processed corpus, I built an LDA model with 5 topics. The topics are  ________________________________________________________________________________________________________________________________________________________________________

* Merge paragraphs from the same books together in the philosophical text corpus.
* Perform LDA, using bigram and trigram models ensure that the LDA utilizes 5 topics
* Create a visualization that depicts each philosophical schools' respective topic prevalence from all 5 topics.
* Reduce the 5-dimensional space to 2 dimensions using Principal Component Analysis (PCA)
* Plot the individual books in this PCA-space (with X and Y axes showing principal component 1 and 2)
* Plot the individual schools in this PCA-space (with X and Y axes showing principal component 1 and 2)
* Save a document showing the most important words for each of the 5 topics

**On a more general level (this applies to all assignments):**

I have tried to as accessible and user-friendly as possible. This has been attempted by the use of:
* Smaller functions. These are intended to solve the sub-tasks of the assignment. This is meant to improve readability of the script, as well as simplifying the use of the script.
* Information prints. Information is printed to the terminal to allow the user to know what is being processed in the background
* Argparsing. Arguments that let the user determine the behaviour and paths of the script (see <a href="#optional-arguments">"Optional arguments"</a> section for more information)

<!-- RESULTS AND DISCUSSION -->
## Results and discussion
Given the exploratory nature of this assignment, little rockhard results have been generated. Instead, an interpretation of the visual output will be presented in this section.

**Topic prevalence in schools of philosophical thought**
<p align="center"><a href="https://github.com/emiltj/cds-language-exam/blob/main/assignment_5/out/plot_topic_prob.png"><img src="./out/plot_topic_prob.png" alt="Logo" width="748" height="512"></a>
  
https://github.com/emiltj/cds-language-exam/blob/main/assignment_5/out/plot_topic_prob.png


**PCA visualizations of schools of philosophical thought**

<p align="center"><a href="https://github.com/emiltj/cds-language-exam/blob/main/assignment_5/out/pca_schools.png"><img src="./out/pca_schools.png" alt="Logo" width="512" height="256"></a>   <a href="https://github.com/emiltj/cds-language-exam/blob/main/assignment_5/out/pca_schools_agg.png"><img src="./out/pca_schools_agg.png" alt="Logo" width="512" height="256"></a></p>

<p align="center"><em>Plot of title topic prevalence (projected onto a 2D PCA space). Colored by school of thought &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Plot of the mean topic prevalence for titles within a philosophical school (projected onto 2D PCA space)</em><p/>

**Words of greatest importance in each topic**

**LDA html output**

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
