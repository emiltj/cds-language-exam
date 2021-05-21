# Assignment 5 - Language Analytics

## Topic of investigation - Topic modeling on a corpus of philosophical texts
I wanted to investigate whether texts from particular schools of philosophical thought, would cluster together in terms of topics. 
I also wanted to see whether texts from the same schools of philosophical thought would cluster together.

## Results of investigation
Visually analyzing the plots produce, it was hard to find clustering of texts from within a philosophical school.
It is also hard to produce meaningful semantic patterns within the topics that the LDA found.

## Content of assignment

This folder contains the following:

| File | Description|
|--------|:-----------|
```topic_modeling_philosophy.py```| A script which is executable from the command-line
```topic_modeling_philosophy_explained.ipynb```| A markdownfile which more clearly explains the process of the script
```out/```| A folder which contains the output from the scripts
```out/lda.html```| __*__ A html which contains the LDA output - weights for each word, and relative placement on a 2-D graph (PCA).
```out/plot_schools_pda.png```| __*__ When taking the mean topic contribution to each school, a generated plot of their PCA component scores.
```out/plot_texts_pda.png```| __*__ A plot of all entries' (all books) PCA component scores, to look for pattern similarity. Colors.
```out/plot_topic_prob.png```| __*__ A plot how much each topic has contributed to texts of a given school.
```out/topic_keywords.csv```| __*__ A .csv file containing the words of each topic.

__* Note that the numbers that correspond to topics are ordered differently in the ```out/lda.html```, as they here have been ordered by importance. See below:__
- 1 in ```out/lda.html``` corresponds to topic 2 in the .png files
- 2 in ```out/lda.html``` corresponds to topic 4 (aristotle's most salient topic) in the .png files
- 3 in ```out/lda.html``` corresponds to topic 3 in the .png files
- 4 in ```out/lda.html``` corresponds to topic 0 in the .png files
- 5 in ```out/lda.html``` corresponds to topic 1 in the .png files


topic_modeling_philosophy.py arguments:
- --edgelist (str - path to input file.  Default = os.path.join("..","data","weighted_edgelist.csv"))

## Running my scripts - MAC/LINUX/WORKER02
Setup
```bash
git clone https://github.com/emiltj/cds-language.git
cd cds-language
bash ./create_lang_venv.sh
```
Running this assignment:
```bash
cd cds-language/assignment_5
source ../lang101/bin/activate 
python topic_modeling_philosophy.py
```

## Running my scripts - WINDOWS
Setup
```bash
git clone https://github.com/emiltj/cds-language.git
cd cds-language
bash ./create_lang_venv_win.sh
```
Running this assignment:
```bash
cd cds-language/assignment_5
source ../lang101/Scripts/activate 
python topic_modeling_philosophy.py
``` 

## Contact

Feel free to write me, Emil Jessen for any questions (also regarding the reviews). 
You can do so on [Slack](https://app.slack.com/client/T01908QBS9X/D01A1LFRDE0) or on [Facebook](https://www.facebook.com/emil.t.jessen/).
