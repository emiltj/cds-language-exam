# Assignment 3 - Language Analytics

## Content of assignment

This folder contains the following:

| File | Description|
|--------|:-----------|
```sentiment.py```| Script that calculates total number of words, as well as total number of unique words for all .txt files within an input folder. The script outputs a .csv file containing rows with this information for each file within the input folder.
```plot_summary.txt```| A short summary which describes what the plots show. Are there any general trends? Can any inferences be drawn from them?
```sentiment_polarity_plot.png```| The output plot, which will be generated given an execution of the script.

sentiment.py arguments:
- --inputpath (str - path to input folder.  Default = os.path.join("..", "data", "abcnews-date-text.csv"))
- --test (bool - Specifies whether to do the analysis on a subset of the data for faster computing. Default = False)

## Running my scripts - MAC/LINUX/WORKER02
Setup
```bash
git clone https://github.com/emiltj/cds-language.git
cd cds-language
bash ./create_lang_venv.sh
```
Running this assignment:
```bash
cd cds-language/assignment_3
source ../lang101/bin/activate 
python sentiment.py
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
cd cds-language/assignment_3
source ../lang101/Scripts/activate 
python sentiment.py
``` 

## Contact

Feel free to write me, Emil Jessen for any questions (also regarding the reviews). 
You can do so on [Slack](https://app.slack.com/client/T01908QBS9X/D01A1LFRDE0) or on [Facebook](https://www.facebook.com/emil.t.jessen/).
