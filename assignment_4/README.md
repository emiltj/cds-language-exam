<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/emiltj/cds-language-exam">
    <img src="../README_images/lang_logo.png" alt="Logo" width="100" height="100">
  </a>
  
  <h2 align="center">Network analysis</h2>

  <p align="center">
    Assignment 4
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
This command-line tool will take a given dataset and perform simple network analysis. In particular, it will build networks based on entities appearing together in the same documents, like we did in class.

Your script should be able to be run from the command line
It should take any weighted edgelist as an input, providing that edgelist is saved as a CSV with the column headers "nodeA", "nodeB"
For any given weighted edgelist given as an input, your script should be used to create a network visualization, which will be saved in a folder called viz.
It should also create a data frame showing the degree, betweenness, and eigenvector centrality for each node. It should save this as a CSV in a folder called output.

* Your script should be able to be run from the command line
* It should take any weighted edgelist as an input, providing that edgelist is saved as a CSV with the column headers "nodeA", "nodeB"
* For any given weighted edgelist given as an input, your script should be used to create a network visualization, which will be saved in a folder called viz.
* It should also create a data frame showing the degree, betweenness, and eigenvector centrality for each node. It should save this as a CSV in a folder called output.

<!-- METHODS -->
## Methods

**Specifically for this assignment:**
A prerequisite for completing this assignment is having a weighted edgelist. I have therefore decided to include an additional script, which generates a weighted edgelist (```create_edgelist.py```). This script takes the ```fake_or_real_news.csv``` dataset and extracts its entities with the label \[PERSON\]. It utilizes the model _en_core_web_sm_ from the SpaCy library. It then find entity pairs (entities that appear within the same document) and counts how often these pairs have appeared in all news articles - these counts are the weight of each of the unique pairs. The weighted edgelist is then saved as a .csv.

The actual assignment script ```network.py``` takes the newly created weighted edgelist as input and the argument _n_ that specifies how many of the heighest weighted node pairs the network analysis should include. It plots the network using the package _networkx_ and saves it to directory ```viz```. It also calculates centrality measures and saves it as a .csv in the folder  ```output```. The measures are eigenvector centrality, betweenness centrality and degree centrality. Eigenvector centrality is a measure of influence of a node - nodes with many connections to other well connected nodes will have higher scores. Betweenness centrality is a measure of centrality in a network - a node that lies on communication flows can control the flow. Calculated by computing the shortest paths between all nodes, then determining the fraction of the number of these paths that go through a given node in question, compared to total number of paths. In a weighted network such as this one, scores are higher given higher edge weights. Degree centrality is merely the number of connections a given node has.

**On a more general level (this applies to all assignments):**
I have tried to as accessible and user-friendly as possible. This has been attempted by the use of:
* Smaller functions. These are intended to solve the sub-tasks of the assignment. This is meant to improve readability of the script, as well as simplifying the use of the script.
* Information prints. Information is printed to the terminal to allow the user to know what is being processed in the background
* Argparsing. Arguments that let the user determine the behaviour and paths of the script (see <a href="#optional-arguments">"Optional arguments"</a> section for more information)

<!-- RESULTS AND DISCUSSION -->
## Results and discussion

**Creating an edgelist:**
|    |                    |                 |        | 
|----|--------------------|-----------------|--------| 
|    | nodeA              | nodeB           | weight | 
| 0  | John F. Kerry      | Kerry           | 21     | 
| 1  | John F. Kerry      | Laurent Fabius  | 2      | 
| 2  | Francois Hollande  | John F. Kerry   | 1      | 
| 3  | John F. Kerry      | Obama           | 76     | 
| 4  | Benjamin Netanyahu | John F. Kerry   | 7      | 
| 5  | Jane Hartley       | John F. Kerry   | 1      | 
| 6  | John F. Kerry      | Victoria Nuland | 1      | 
| 7  | Eric H. Holder Jr. | John F. Kerry   | 1      | 
| 8  | John F. Kerry      | Narendra Modi   | 1      | 
| 9  | Kerry              | Laurent Fabius  | 12     | 
| 10 | Francois Hollande  | Kerry           | 17     | 

<em>The head of the output edgelist - generated from the script</em>

As can be seen in the table above, the script for generating weighted edgelists has been sucessfully in that it indeed has created a weighted edgelist. The entity extraction of people has correctly both identified John F. Kerry and Kerry as entities. As can be seen in the table however, the script was not programmed to merge entities referring to the save person into a single entity, i.e. changing "Kerry" into "John F. Kerry" to avoid the problem we see above. Additional processing ought to have been carried out to circumvent this problem.

**Network analysis:**
<p align="center"><a href="https://github.com/emiltj/cds-language-exam/blob/main/assignment_4/out/viz/network_visualization.png"><img src="./out/viz/network_visualization.png" alt="Logo" width="700" height="512"></a></p>
<p align="center"><em>The network visualized</em><p/>

|    |                 |                        |                        |                     | 
|----|-----------------|------------------------|------------------------|---------------------| 
|    | node            | eigenvector_centrality | betweenness_centrality | degree_centrality   | 
| 0  | Clinton         | 0.5276992157079976     | 0.7087912087912088     | 0.8571428571428571  | 
| 1  | Trump           | 0.5359784095931499     | 0.4670329670329671     | 0.6428571428571428  | 
| 2  | Obama           | 0.2877321039031794     | 0.0                    | 0.2857142857142857  | 
| 3  | Hillary Clinton | 0.22647028527916035    | 0.0                    | 0.14285714285714285 | 
| 4  | Bush            | 0.23017534121767486    | 0.14285714285714288    | 0.3571428571428571  | 
| 5  | Cruz            | 0.21691893908246254    | 0.0                    | 0.2857142857142857  | 
| 6  | Donald Trump    | 0.22647028527916035    | 0.0                    | 0.14285714285714285 | 
| 7  | Hillary         | 0.11235411372791775    | 0.0                    | 0.07142857142857142 | 
| 8  | Rubio           | 0.2659257043545763     | 0.01098901098901099    | 0.3571428571428571  | 
| 9  | Bill Clinton    | 0.11235411372791775    | 0.0                    | 0.07142857142857142 | 
| 10 | Clintons        | 0.11235411372791775    | 0.0                    | 0.07142857142857142 | 

<p align="center"><em>Centrality measures</em><p/>


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
