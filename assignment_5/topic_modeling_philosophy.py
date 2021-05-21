#!/usr/bin/python

############################## Importing libraries ###############################
import sys, os, random, spacy, nltk, gensim, logging, warnings, gensim, argparse
sys.path.append(os.path.join(".."))
import pandas as pd
import gensim.corpora as corpora
import pandas as pd
import pyLDAvis.gensim
import seaborn as sns
import matplotlib as plt
from matplotlib import rcParams
from nltk.corpus import stopwords
from pprint import pprint
from sklearn.decomposition import PCA
from gensim.models import CoherenceModel
from utils import lda_utils

# Import and set various parameters
nlp = spacy.load("en_core_web_sm", disable = ["ner"])
nlp.max_length = 10000000
stop_words = stopwords.words('english')
pd.reset_option('^display.', silent=True)
sns.set_theme()
rcParams['figure.figsize'] = 20,10
warnings.filterwarnings('ignore')
logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.ERROR)
random.seed(1023)

############################## Defining functions to be used in main ##############################
def print_lda_performance(lda_model, corpus, texts_processed, diction):
    '''
    Function that prints LDA model performance on the measures of Perplexity and Coherence score
    '''
    # Compute and print perplexity score
    print(f"[PERFORMANCE INFO] LDA model has a perplexity score of: {lda_model.log_perplexity(corpus)}")  # A measure of how good the model is. lower the better.
    
    coherence_model_lda = CoherenceModel(model = lda_model, 
                                     texts = texts_processed, 
                                     dictionary = diction, 
                                     coherence = 'c_v')
    
    # Compute and print coherence score
    coherence_lda = coherence_model_lda.get_coherence()
    print(f"[PERFORMANCE INFO] LDA model has a coherence score of: {coherence_lda}")
    
def get_topic_prevalence(lda_model, corpus):
    '''
    Function which retrieves information about topic prevalence in a given corpus, for a given LDA model.
    Output is a list of lists, containing information about topic prevalence in the corpus in the format:
    [[<entry 1's topic 0 score>, <entry 2's topic 0 score> ... ], [<entry 1's topic 1 score>, <entry 2's topic 1 score> ...] ...]
    '''
    # Creates a list of lists of a list of tuples. 
    # Each entry has a sublist, and each contain a list of tuples. 
    # Each tuple indicate the likelihood of an entry being generated from each topic.
    # E.g. [[(topic_0, 4.8436028e-05), (topic_1, 4.8412476e-05)],[(topic_0, 0.024443716), (topic_1, 0.8044679),]]
    topic_prevelance_tuples = list(lda_model.get_document_topics(corpus))
    
    # Using the below loop; format to [[4.8436028e-05, 4.8412476e-05], [0.024443716, 0.8044679]], instead.
    # Empty list for appending to
    text_topic_prevelance = []

    # For each text entry topic prevalence tuples
    for entry in topic_prevelance_tuples:

        # Empty list for appending topic prevelance for each entry
        topic_prevelance = []

        # For each topic in entry append the likelihood to topic prevalence
        for topic in entry:

            # Append likelihood ([1] to not include index for likelihood)
            topic_prevelance.append(topic[1])

        # Append topic prevelance likelihood to overall list
        text_topic_prevelance.append(topic_prevelance)
    
    # Using below loop, format to [[<entry 1's topic 0 score>, <entry 2's topic 0 score> ... ], [<entry 1's topic 1 score>, <entry 2's topic 1 score> ...] ..]

    # Empty list for appending to
    topic_prevelance = []

    # For i in 0, 1, 2, 3, 4
    for i in range(0, 5):
        topic_prevelance.append([item[i] for item in text_topic_prevelance])
        
    # Return topic prevalence
    return topic_prevelance

def topic_prob_plot(df, group, title, outname):
    '''
    Function that creates and saves a scatterplot of a dataset with topic probability scores. 
    Takes argument group (which group to group by), title (title of plot) and outname (name for output file).
    '''
    # Create plot over the different philosophical schools' aggregated topic probability distributions
    plot_topic_prob = sns.scatterplot(data = df.groupby(group).mean().T).set_title(title)
    plot_topic_prob

    # If the folder does not already exist, create it
    if not os.path.exists("out"):
        os.makedirs("out")
    
    # Saving to folder
    outpath = os.path.join("out", outname)
    plot_topic_prob.get_figure().savefig(outpath)
    print(f"[INFO] A new file has been created successfully \"{outpath}\"") # Info for terminal
    
    
def pca_plot(df, group, title, outname):
    '''
    Function that creates and saves a relplot of a PCA dataset (df).
    Takes argument group (which group to group by), title (title of plot) and outname (name for output file).
    '''
    pca_plot = sns.relplot(
    data = df,
    x = "principal component 1", y = "principal component 2", hue = group).fig.suptitle("")
    
    # If the folder does not already exist, create it
    if not os.path.exists("out"):
        os.makedirs("out")
    
    # Saving to folder
    outpath = os.path.join("out", outname)
    pca_plot.get_figure().savefig(outpath)
    print(f"[INFO] A new file has been created successfully \"{outpath}\"") # Info for terminal
    
############################## Defining main function ##############################
def main(inpath, subset):
    '''
    Main function of the script
    '''
    # Reading the philosophy data
    df = pd.read_csv(inpath)

    # Running on subset of "only" 50000 entries for faster processing
    if subset == True:
        df = df[["title", "author", "school", "sentence_lowered"]].sample(50000)

    # The dataset contains multiple entries from the same books. This can be problematic for performing LDA.
    # Therefore: create new pandas series, with all texts from same book title titles joined
    sentence_lowered_agg = df.groupby(['title'])['sentence_lowered'].apply(lambda x: ' '.join(x)).reset_index()["sentence_lowered"]

    # Ensure that df only contains one entry of each title (since we have acquired all text per title)
    df = df.drop_duplicates(subset = ["title"])

    # Insert the text which has been aggregated per title
    df["sentence_lowered"] = list(sentence_lowered_agg)

    # Build bigram and trigram models
    print(f"[INFO] Building bigram and trigram models (preparing for LDA) ...") # Info for terminal
    bigram = gensim.models.Phrases(df["sentence_lowered"], min_count=5, threshold=100) # Higher threshold means fewer phrases
    trigram = gensim.models.Phrases(bigram[df["sentence_lowered"]], min_count = 1, threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    # Acquire a list of lists. Each of these lists contain all unique words that have one of the postags: 'NOUN', "ADJ", "VERB", "ADV"
    texts_processed = lda_utils.process_words(df["sentence_lowered"], nlp, bigram_mod, trigram_mod,
                                             allowed_postags=['NOUN']) # Only consider certain postags.

    # Create dictionary (converting each word into an integer value, which functions like an ID)
    id2word = corpora.Dictionary(texts_processed)

    # Create corpus of Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts_processed]

    # Build an LDA model
    print(f"[INFO] Creating LDA model ...") # Info for terminal
    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics= 5, 
                                           random_state=100,
                                           chunksize=10,
                                           passes=10,
                                           iterations=100,
                                           per_word_topics=True, 
                                           minimum_probability=0.0)

    # Getting LDA performance and printing
    print_lda_performance(lda_model, corpus, texts_processed, id2word)

    # Create data frame with information topic keywords and which entries have which dominant topic.
    df_topic_keywords = lda_utils.format_topics_sentences(ldamodel=lda_model, 
                                                          corpus=corpus, 
                                                          texts=texts_processed)

    # Merge topic dataframe with the philosophical entries
    df_topic_keywords = df.reset_index(drop = True).join(df_topic_keywords)

    # Change column name from "0" to "text_tokenized"
    df_topic_keywords.rename(columns={df_topic_keywords.columns[7]: "Text_Tokenized" }, inplace = True)

    # Calculate topic prevalence in each topic, for each entry
    topic_prevalence = get_topic_prevalence(lda_model, corpus)

    # Add topic prevalence for each topic to entries using the below loop:
    # Initialize counter
    counter = 0

    # For each entry in the original dataset, create a new column containing topic prevelance
    for topic in topic_prevalence:

        # For topic 0 add prevalence scores to new column with name "0", etc.
        df_topic_keywords[f"{counter}"] = topic

        # Next topic
        counter += 1

    # For each unique dominant topic, show the columns dominant topic + topic keywords
    topic_keywords = df_topic_keywords.drop_duplicates(subset = ["Dominant_Topic"]).loc[:,["Dominant_Topic", "Topic_Keywords"]]

    # Perform PCA - reducing our feature space to 2 dimensions:
    pca = PCA(n_components=2)

    # Fit transform to get PCA components
    print(f"[INFO] Performing PCA dimensionality reduction for visualizations ...") # Info for terminal
    principal_components_school = pca.fit_transform(df_topic_keywords[["0", "1", "2", "3", "4"]])
    principal_components_school = pd.DataFrame(data = principal_components_school, columns = ['principal component 1', 'principal component 2'])

    # Add "school" onto the principal components data frame
    principal_components_school["school"] = df_topic_keywords["school"]

    # Creating a new dataframe with the aggregated mean scores of each school
    principal_components_school_agg = principal_components_school.groupby("school").mean()

    # Saving to out folder
    topic_keywords.to_csv(os.path.join("out", "topic_keywords.csv"), index=False)

    # Plotting and saving the topic prevalence in each of the 10 schools
    topic_prob_plot(df_topic_keywords.set_index("school")[["0", "1", "2", "3", "4"]], 
                    "school", 
                    "Philosophical schools' topic probability distributions", 
                    "plot_topic_prob.png")

    # Plotting and saving a PCA_plot reduced to two dimensions. Grouping by school, but showing individual points for each title
    pca_plot(principal_components_school, "school", "Texts by school in topic model space (reduced to 2D PCA)", "pca_schools.png")

    # Plotting and saving a PCA_plot reduced to two dimensions. Grouping by school and showing a single point for each school
    pca_plot(principal_components_school_agg, "school", "Aggregated texts within school in topic model space (reduced to 2D PCA)", "pca_schools_agg.png")

    # Here looking at the intertopic distance + which tokens are most salient/important for each topic.  ***NOTE***
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary = lda_model.id2word)
    # *** The numbers in the vis do not correspond to the number labels of the topics in the other visualizations.
    # Why?
    # The vis here is ordered by importance for the entire dataset - look at the words contained within each topic to map them onto the previous visualizations

    # Saving the visualization (interactive html)
    outpath = os.path.join("out", "lda.html")
    pyLDAvis.save_html(vis, outpath)
    print(f"[INFO] A new file has been created successfully \"{outpath}\"") # Info for terminal

############################## Defining behaviour when called from command line ##############################
if __name__=="__main__":
    # Initialize ArgumentParser class
    parser = argparse.ArgumentParser(description = "[SCRIPT DESCRIPTION] Perform LDA on the philosophical texts' data set and visualization the relationship between the different philosophical schools")
    
    # Add inpath argument
    parser.add_argument(
        "-i",
        "--inpath", 
        type = str,
        default = os.path.join("data", "philosophy_data.csv"), # Default path to data
        required = False,
        help= "str - path to image corpus")
    
    # Add subset argument
    parser.add_argument(
        "-s",
        "--subset", 
        type = bool,
        default = True,
        required = False,
        help= "bool - specifying whether to run only on a subset of 50000 randomly sampled entries or on the full dataset")
    
    # Taking all the arguments we added to the parser and input into "args"
    args = parser.parse_args()
    
    # Perform main function
    main(args.inpath, args.subset)