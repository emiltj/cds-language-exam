<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/emiltj/cds-language-exam">
    <img src="../README_images/lang_logo.png" alt="Logo" width="100" height="100">
  </a>
  
  <h2 align="center">LSTM models for text generation (self-assigned)</h2>

  <p align="center">
    Assignment 7
    <br />
    <a href="https://github.com/emiltj/cds-language-exam/issues">Report Bug</a>
    ·
    <a href="https://github.com/emiltj/cds-language-exam/issues">Request Feature</a>
  </p><
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

This assignment seeks to investigate an approach to generate new textual content. It implements a Recurrent Neural Network (RNN) to learn word sequence patterns. Using the trained model new word sequences are generated.

More specifically, this assignment seeks see whether it is possible to generate new textual content in line with the text from [the corpus](https://www.kaggle.com/tschomacker/grimms-fairy-tales) of folklore fairy tales written by the Brothers Grimm (Jacob Ludwig Karl Grimm and Wilhelm Carl Grimm). The project intends to investigate the questions: _How well can a neural network learn the patterns of the writings of the Brothers Grimm?_ and _Using the trained model - is it possible to generate new textual content that could have been something you might read in an old fairy tale?_

Try using a text generative approach that learns and predicts on word-level, rather than on a character-level.

* Train a Long Short-Term Memory (LTSM) artificial Recurrent Neural Network (RNN) on the corpus
* Use sequences of 50 words as input for the model
* Generate new sequences of texts, using the trained model
* Bonus task: include arguments that let you specify model training parameters and LTSM model architecture (LTSM layers, epochs and batch size). You might also want to specify options for the text generation - how many text chunks should be generated?

<!-- METHODS -->
## Methods

**Specifically for this assignment:**

For this assignment I started out by loading in the text corpus. The text was then preprocessed; the strings that each contained a fairy tale were combined into a single string, which was divided up into a list of words. The preprocessing also entailed the removement of non-alphanumeric characters which meant that line breaks, punctuation and quotations marks were removed. I then defined and made use of a function which retrieves word sequences using a moving window, this function took window-size and step-size as arguments. To give an example: Given window-size = 3 and step-size = 1, it would retrieve the sequences [["once upon a"], ["upon a time"], ["a time in"]] from the text ["once", "upon", "a", "time", "in"].
For this analysis, the sequences retrieved from the Grimms' fairy tales would be of length 51 and would move by a single word at a time. The sequences were then tokenized meaning that the list of words was converted into a vector. The integers of the vector were unique for each word and functioned as an ID in a saved vocabulary list, enabling the vectors to be converted back into words. Having the text sequences as vectors allow the model in training on the data. 
The first 50 words in each tokenized sequence would be used as features for the model input, while the last word in the sequence would be what the model tries to predict. Before training, the tokens to be predicted were one-hot encoded, to allow for the model to use categorical crossentropy as loss function and softmax activation for the final layer. This way, the model would return an array of the probability of each of the possible predictions. The word with the highest probability would then be used as the prediction of the model.

<p align="center">
<a href="https://github.com/emiltj/cds-language-exam/README_images/text_generation_pipeline.png">
<img src="../README_images/text_generation_pipeline.png" alt="Logo" width="538" height="296">
</a>

<p align="center"><em>Visualization of the pipeline used for text generation</em></p>

The model consists of an embedding layer followed by two LTSM layers of depth 128 and 100 as per default. Using the argument _--ltsmlayers_, one may specify another structure for the LTSM layers. The model implements LTSM layers due to their way of handling the vanishing gradient problem (the problem of shrinking gradients over time in backpropagation) that is prevalent in traditional RNNs. It does so by the use of feedback connections called gates. The LTSM layers are succeeded by a dense layer of 32 nodes and an output layer with a softmax activation function with number of nodes equal to number of possible predictions (number of unique words in the corpus).
During model training, the model adjusts its' weights in order to learn the patterns in the sequences. This enables it in predicting the next token that would appear after each sequence of 50 tokens. Epochs and batchsize for the model training can be determined using the arguments _--epochs_ and _--batchsize_ (see section "Optional arguments" for more information).

<p align="center">
<a href="https://github.com/emiltj/cds-language-exam/README_images/text_generative_models.png">
<img src="../README_images/text_generative_models.png" alt="Logo" width="860" height="296">
</a>

<p align="center"><em>Visualization of the principle behind text generation algorithms. Image from blogpost by Harsh Basnal (https://bansalh944.medium.com/text-generation-using-lstm-b6ced8629b03) </em></p>

How can a model that classifies the next word in a sequence be used to generate new text? A visualization of text generation approach used in this script can be seen above. First it takes a sequence of words (a seed-sequence) and predict which word is the most likely to succeed. The model then uses all words in the seed-sequence except the first, plus the newly predicted word to predict another new word. Followed by a new prediction of the seed-sequence except the first two first, plus the two newly predicted words. This continues until the model has predicted and thus generated a new sequence of some specified length. It must be mentioned that the model does not do this with words, but rather with the integer values as the strings have been vectorized. Upon the completion of generating a new sequence in vector format, the tokens that all carry a unique ID are converted back into words using the saved dictionary of integer ID to word.

The seed-sequences used to generate text in this script are the same sequences that were used to train the model. When generating a new sequence the script samples from these sequences random. The number of generated sequences can be specified using the argument _--ngenerate_.

**On a more general level (this applies to all assignments):**

I have tried to as accessible and user-friendly as possible. This has been attempted by the use of:
* Smaller functions. These are intended to solve the sub-tasks of the assignment. This is meant to improve readability of the script, as well as simplifying the use of the script.
* Information prints. Information is printed to the terminal to allow the user to know what is being processed in the background
* Argparsing. Arguments that let the user determine the behaviour and paths of the script (see <a href="#optional-arguments">"Optional arguments"</a> section for more information)

<!-- RESULTS AND DISCUSSION -->
## Results and discussion

**Model training**

The model achieved a training accuracy of 64% which means that more than half of the word predictions were correct. Given the +2700 classes (unique words, possible to predict) it can be said that the model performed quite well. Needless to say, this is certainly because the model overfit the the data set. It learned patterns that are specific to these texts, rather than patterns that would apply to all texts. If tested on out-of-sample texts, the performance would evidently drop significantly as a result of the low generalizability. However, the purpose of this model was not generalize to other texts and to achieve high out-of-sample performance, but rather to generate texts. But did the model train enough? From looking at the plot over training accuracy and loss over epochs, it appears that the model had diminishing returns as epochs increased and more epochs would likely not have increase performance much. Given a more complex model architecture, the ceiling effect of performance may have occurred later. If such a model had been trained for more epochs, the models may have been able to perform even better.

<p align="center">
<a href="https://github.com/emiltj/cds-language-exam/blob/main/assignment_7/out/training_hist.png">
<img src="out/training_hist.png" alt="Logo" width="300" height="200">
</a>

<p align="center"><em>Training history of the model</em></p>

**Generated text output**

For clarificational purposes, I will go through two examples of generated sequences for this section. The full output of generated sequences can be found in ```assignment_7/out/generated_sequences.csv``` and an excerpt of this table can be found at the bottom of this section.

After manually altering two generated sequences that the model ended up producing, here are some examples of the output:

> [...] He took them a powerful gold, lying on the floor and nailed them free. 
> The fifth in day, she went to bed then he went into the kitchen and said to him: "Can you light nothing but set me free". Wash it sleeping and did not believe that it might soon as it were. [...]"


<p align="center"><em>Example 1 - formatted</em></a>

> [...] "The sun soon wanted to drink. The door was a poor pity and he got up into the room and wanted to have", said the king. 
> As he came towards it and sat down on her head and did not fly about, the wolf knocked into the water and kill her. [...]


<p align="center"><em>Example 2 - formatted</em></a>

Note that these have been manually altered by adding line breaks, punctuation and by capitalizing letters after periods. The sentences seem to apply to some rules of grammar; verbs seem to be predicted in the context of nouns. Determiners such as "the" seems to accurately precede nouns, while prepositions such as "on" and "to" are correctly placed in sentences such as "_lying on the floor_" and "_she went to bed_". Although the generated content had some merits in terms of grammaticical structure, there are also pitfalls. The model seems to arbitrarily guess whether a word should appear in its past of present tense - "_the wolf knocked into the water an kill her_". Furthermore almost all semantic coherence seems to be absent. A sentence such as "_The sun soon wanted to drink._" does not make much sense. Not even when read in the context of fairy tales which is what the text is meant to resemble.
Lack of semantic coherence seems to be a general issue across the different methods used to generate new text - even for esteemed experts in RNNs such as the team behind TensorFlow (see their approach [here](https://www.tensorflow.org/text/tutorials/text_generation)). At present, text generative processes seem to be mostly useful for entertainment purposes, generating abstract poetry or as a means to acquire inspirational content in an atypical way. When looking at the raw output of the script it also becomes evident that this model lacks the formatting that was manually applied in the two previous examples - things such as line breaks, punctuation and capitalization of letters after periods. Take a look at the examples in their unformatted raw version below (for the entire output, see [generated_sequences.csv](https://github.com/emiltj/cds-language-exam/blob/main/assignment_7/out/generated_sequences.csv)).

> [...] he took them a powerful gold lying on the floor and nailed them free the fifth in day she went to bed then he went into the kitchen and said to him can you light nothing but set me free wash it sleeping and did not believe that it might soon as it were [...]


<p align="center"><em>Example 1 - raw</em></a>

> [...] the sun soon wanted to drink the door was a poor pity and he got up into the room and wanted to have said the king as he came towards it and sat down on her head and did not fly about the wolf knocked into the water and kill her [...]


<p align="center"><em>Example 2 - raw</em></a>

The results leave us with some information to answer the two questions posed in the description of the project: "_How well can a neural network learn the patterns of the writings of the Brothers Grimm?_" and "_Using the trained model - is it possible to generate new textual content that could have been something you read in an old fairy tale?_". It seems that this specific neural network can learn some patterns of fairy tales and of language in general. Given that the model has had no hard-coded rules implemented it can be thought impressive that it was able to produce sequences of text with a least some grammatical structure. However, it is clear that the model is not able to generate new textual content that one might have read in a fairy tale from the 1810s, as there seems to be little to no meaning in the produced texts. Moreover, the preprocessing of the data filtered away non-alphanumeric characters and this may have been unnecessary. Had, for instance, periods been treated like tokens just as the words, the model may had been able to predict punctuation somewhat accurately. Pair this with line breaks and quotation marks etc., and the output produced may have resembled text in fairy tales slightly more accurately. Other measures might also have been taken, such as applying Regex patterning to capitalize the first letter following a period.


|    |                                                               |                                                                                                                                                                            | 
|----|---------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
|    | length_10                                                     | length_50                                                                                                                                                                  | 
| 0  | from whence his wealth came to see them to the                | her own child will for this then the king went shivering and looked up and saw that their hair her sister loved his bread she thought each man caused found                | 
| 1  | cried is himself give me my head then the king                | brought two far in the window and the man came with pale and diamonds equipped a thousand folk this cages loudly and as he saw a white snake lying coiled                  | 
| 2  | kitchen and shook out the willowwren flew up to his           | has supported me down into the cellar and see where my father grieved when we to eat of the sexton came to the door he leapt into the inn there                            | 
| 3  | foot and limped hobblety jib hobblety and when he came        | him joy at once the king had a great thirst and mother so she sat down by the fields and then he ran back to her grave and said what                                       | 
| 4  | and when he had gone on her she walked out                    | dead an old fox too for she began to bewail them began with gold and sleep dogs yet fiddle and then her mother should find him as he could even                            | 
| 5  | place and when he saw the bridegroom screamed out and         | after something but that you can have my thirst but happen to said the youth and was travelling dead cup to the bottom of the movements door remained a raven              | 
| 6  | man reappeared is all said the king will keep awake           | the head and every day was a great thing that was called someone and he did not know what to do what they darling sighing and shoes held over the                          | 
| 7  | brought it up and then went to the old fox                    | it about and the cook heard all they heard him much that nevertheless on sides before it to pass but dame than it and was very tired she sat herself                       | 
| 8  | behind the end of the wood the dwarf went into                | the only elder must have carried up one rich calling to her there lies the nightingale was disenchanted for the house of the sun it said must have a false                 | 
| 9  | in use of where he were going loudly before at                | ought to have any purpose in the court can be gone and speak very drop and was carried up into the mountains and dig him singing to pry and chanticleer                    | 
| 10 | away one night the king drew the order down the               | dressed themselves on the shore soon said queen aloud depend for here trip bound to procure get at the table and when he awoke from the meantime window he thought         | 
| 11 | however in the middle of the well briar opened the            | content as soon as he had heard all many that they had been the power of the chickens and were sentenced birth to a gardener and went to bed then                          | 
| 12 | ought to see her and the limbs was promised two               | blood on heaven and was very fond of his finger and took after a white stable from his pipe by the courtyard and chambers long calling and while the daughter              | 
| 13 | floor till the spot he called her horse and turned            | white as that i will get the water for have been handling one of these with your way so she took the first bar of his legs and partlet saw                                 | 
| 14 | bear took him out of the stream and called behind             | stays are laced let me lace them down with my shoes as if you want to learn to the third little cat is no longer said she and gold am                                      | 
| 15 | cried out because i should have no good and when              | that he went on and took a hatchet and ate before her and complained that day was a wonderful mountain wretch that he found a hair looking down but the                    | 

<!-- USAGE -->
## Usage

Make sure to follow the instructions in the README.md located at the parent level of this repository, for the required installation of the virtual environment as well as the data download.

Subsequently, use the following code (when within the ```cds-language-exam``` folder):

```bash
cd assignment_7
source ../lang101/bin/activate # If not already activated
python text_generator.py
```

### Optional arguments:

text_generator.py arguments for commandline to consider:
-       "-i",
        "--inpath", 
        type = str,
        default = os.path.join("data", "grimms_fairytales.csv"),
        required = False,
        help = "str - specifying inpath to the Grimms fairy tales")
-       "-l",
        "--ltsmlayers", 
        type = int,
        nargs='+',
        default = [128, 100],
        required = False,
        help = "list of integers - specifying number and depth of LTSM layers. e.g. --ltsmlayers 32, 64, 32")
-       "-b",
        "--batchsize", 
        type = int,
        default = 64,
        required = False,
        help = "int - specifying batch size for the model training")
-       "-e",
        "--epochs", 
        type = int,
        default = 350,
        required = False,
        help = "int - specifying number of epochs for the training")
-       "-n",
        "--ngenerate", 
        type = int,
        default = 50,
        required = False,
        help = "int - specifying how many sequences the script should generate")

<!-- CONTACT -->
## Contact

Feel free to write me, Emil Jessen for any questions.
You can do so on [Slack](https://app.slack.com/client/T01908QBS9X/D01A1LFRDE0) or on [Facebook](https://www.facebook.com/emil.t.jessen/).

