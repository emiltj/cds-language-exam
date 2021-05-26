<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/emiltj/cds-language-exam">
    <img src="../README_images/lang_logo.png" alt="Logo" width="100" height="100">
  </a>
  
  <h2 align="center">LSTM models for text generation</h2>

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

This assignment seeks to generative new textual content by implementing a Recurrent Neural Network (RNN). More specifically, this assignment seeks see whether it is possible to generate new textual content in line with the text from [the corpus](https://www.kaggle.com/tschomacker/grimms-fairy-tales) of folklore fairy tales written by the Brothers Grimm (Jacob Ludwig Karl Grimm and Wilhelm Carl Grimm). The project intends to investigate the questions: _How well can a neural network learn the patterns of the writings of the Brothers Grimm?_ and _Using the trained model - is it possible to generate new textual content that could have been something you read in an old fairy tale?_

Try using a text generative approach that learns and predicts on word-level, rather than on a character-level.

* Train a Long Short-Term Memory (LTSM) artificial Recurrent Neural Network (RNN) on the corpus
* Use sequences of 50 words as input for the model
* Bonus task: include arguments that let you specify model training parameters and LTSM model architecture (LTSM layers, epochs and batch size). You might also want to specify options for the text generation - how many text chunks should be generated?

<!-- METHODS -->
## Methods

**Specifically for this assignment:**

For this assignment I started out by loading in the text corpus. The text was then preprocessed; the strings that each contained a fairy tale were appended to one long list of strings (each item in the list being one word). During preprocessing non-alphanumeric characters and linebreaks were also removed. I then defined and made use of a function retrieves word sequences using a moving window (e.g. ["once", "upon", "a", "time", "in"] becomes the sequences: [["once upon a"], ["upon a time"], ["a time in"]] when using window size = 3 and step size = 1). I chose to retrieve sequences of size 51.  The sequences were then tokenized meaning that each word was replaced by an integer and that the specific integer also functions as an ID in a saved vocabulary list. Having the text sequences as this array allow the model to train on the data. 
The first 50 words in each tokenized sequence would be used as features for the model input, while the last word in the sequence would be what the model tries to predict. The list of tokens to predict are then one-hot encoded to match the shape for a keras model that uses categorical crossentropy as loss function and softmax activation for the final layer.

<p align="center">
<a href="https://github.com/emiltj/cds-language-exam/README_images/text_generation_pipeline.png">
<img src="../README_images/text_generation_pipeline.png" alt="Logo" width="538" height="296">
</a>

<p align="center"><em>Visualization of the pipeline used for text generation</em></p>

The model consists of an embedding layer followed by two LTSM layers of depth 128 and 100 as per default. Using the argument --l, one may specify another structure for the LTSM layers. The model implements LTSM layers due to their way of handling the vanishing gradient problem (the problem of shrinking gradients over time in backpropagation) that is prevalent in traditional RNNs. It does so by the use of feedback connections called gates. The LTSM layers are succeeded by a dense layer (32 nodes) and an output layer that uses softmax and has the number of nodes equal to number of possible predictions (number of unique words in the corpus).
The model is then trained on the data, learning the patterns in the sequences to be able to predict the next token that would appear after each sequence of 50 tokens. Epochs and batchsize for the model training can be determined using the arguments (see section "Optional arguments").

<p align="center">
<a href="https://github.com/emiltj/cds-language-exam/README_images/text_generative_models.png">
<img src="../README_images/text_generative_models.png" alt="Logo" width="860" height="296">
</a>

<p align="center"><em>Visualization of the principle behind text generation algorithms. Image from blogpost by Harsh Basnal (https://bansalh944.medium.com/text-generation-using-lstm-b6ced8629b03) </em></p>

The text generation method works by taking a sequence of tokens of the same length as the input layer (e.g. one of the sequences of 50 words that were used to train the model) and predict the next token using the trained model. This word prediction is the first token of the sequence that is to be generated. The model then uses the 49 last tokens of the input sequence plus the newly predicted token to predict the next token. And so on an so forth, until the requirements for length of the generated sequence has been met. Since the tokens all carry a unique ID, the actual words that the point to can be identified using the saved ID-word dictionary. 

The script uses the above mentioned principle to generate new sequences. It randomly samples sequences from the training data to generate the new texts. The number of generated sequences can be specified using the argument _--ngenerate_.

**On a more general level (this applies to all assignments):**

I have tried to as accessible and user-friendly as possible. This has been attempted by the use of:
* Smaller functions. These are intended to solve the sub-tasks of the assignment. This is meant to improve readability of the script, as well as simplifying the use of the script.
* Information prints. Information is printed to the terminal to allow the user to know what is being processed in the background
* Argparsing. Arguments that let the user determine the behaviour and paths of the script (see <a href="#optional-arguments">"Optional arguments"</a> section for more information)

<!-- RESULTS AND DISCUSSION -->
## Results and discussion

**Model training**

The model achieved a training accuracy of 64% - mean that more than half the of the word predictions were correct. Given the +2700 classes (unique words to predict) it can be said that the model performed quite well. Needless to say, this is certainly because the model overfit to this data, be learning patterns that are specific to this dataset. Evidently, the performance when predicting out of the training samples would drop significantly as the model would not generalize well. However, the purpose of this model was not generalize to other texts and to achieve high out-of-sample accuracies, but rather to generate texts. But did the model train enough? From looking at the plot over training accuracy and loss over epochs, it appears that the model had diminishing returns as epochs increased and more epochs would likely not have increase performance much. Although perhaps given a more complex architecture, the model have been able to perform even better on the training data given more epochs.

<p align="center">
<a href="https://github.com/emiltj/cds-language-exam/blob/main/assignment_7/out/training_hist.png">
<img src="out/training_hist.png" alt="Logo" width="300" height="200">
</a>

<p align="center"><em>Training history of the model</em></p>

**Generated text output**

After manually altering two cherry-picked results that the model ended up producing, we're left with two examples:

<p align="center">
  
> [...] He took them a powerful gold, lying on the floor and nailed them free. 
> The fifth in day, she went to bed then he went into the kitchen and said to him: "Can you light nothing but set me free". Wash it sleeping and did not believe that it might soon as it were. [...]"

> [...] "The sun soon wanted to drink. The door was a poor pity, and he got up into the room and wanted to have", said the king. 
> As he came towards it and sat down on her head and did not fly about, the wolf knocked into the water and kill her. [...]
</p>

Note that these have been manually altered by adding linebreaks, punctuation and by capitalizing letters after periods. The sentences seem to apply to some rules of grammar; verbs seem to be produce in the context of nouns while the determiner "the" seems to accurately preceeed nouns. Although the generated content had some merits in terms of grammatic structure, semantic coherence seems to be absent. A sentence such as "The sun soon wanted to drink." does not make much sense - it is even a bit farfetched when viewed in the context of fairy tales, which is what the text is meant to resemble.
Lack of semantic coherence seems to be a general issue across the different methods used to generate new text - even for esteemed experts in RNNs such as the team behind TensorFlow (see their approach [here](https://www.tensorflow.org/text/tutorials/text_generation)). At present, text generative processes seem to be mostly useful for entertainment purposes, abstract poetry, or as a means to acquire inspirational content in an atypical way. When looking at the raw output of the script, it also becomes evident that this model lacks the formatting that was manually applied in the two previous examples - things suchs as linebreaks, punctuation and capitalization of letters after periods. Take a look at the unformatted raw output below.

> [...] he took them a powerful gold lying on the floor and nailed them free the fifth in day she went to bed then he went into the kitchen and said to him can you light nothing but set me free wash it sleeping and did not believe that it might soon as it were [...]

> [...] the sun soon wanted to drink the door was a poor pity and he got up into the room and wanted to have said the king as he came towards it and sat down on her head and did not fly about the wolf knocked into the water and kill her [...]

The results leave us with some information to answer the two questions posed in the description of the project: "_How well can a neural network learn the patterns of the writings of the Brothers Grimm?_" and "_Using the trained model - is it possible to generate new textual content that could have been something you read in an old fairy tale?_". It seems that this specific neural network can learn some patterns of fairy tales and of language in general. Given that the model has had no hard-coded rules implemented it can be thought impressive that it was able to produce sequences of text with a least some grammatical structure. However, it is clear that the model is not able to generate new textual content that one might have read in a fairy tale from the 1810s, as there seems to be little to no meaning in the produced texts. Moreover, the preprocessing of the data filtered away non-alphanumeric characters and this may have been unnecessary. Had, for instance, periods been treated like tokens just as the words, the model may had been able to predict punctuation somewhat accurately. Pair this with linebreaks and quotation marks etc., and the output produced may have resembled text in fairy tales slightly more accurately. Other measures might also have been taken, such as applying regex patterning to capitalize the first letter following a period.

|    |                                                               |                                                                                                                                                                            |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | 
|----|---------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| 
|    | length_10                                                     | length_50                                                                                                                                                                  | length_200                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | 
| 0  | from whence his wealth came to see them to the                | her own child will for this then the king went shivering and looked up and saw that their hair her sister loved his bread she thought each man caused found                | free in the middle of the sea and brought down some pair he took them a powerful gold lying on the floor and nailed them free the fifth in day she went to bed then he went into the kitchen and said to him can you light nothing but set me free wash it sleeping and did not believe that it might soon as it were a very king of the guests who was going by people that she had walked in her side might refresh him after him she could make and hansel burst her more at the lion now could not be carried for work on he saw that it might know of a bear you have given her allowed to be true the most merchant who was there you will not see his dinner in the work might have rained leave she went out behind her hand and said are not to then they searched and wants to say goodbye together lies a long way safe and cheese as he was willing and was very good the other large plaything and she came her two daughters and as she was going to drink the man gave the                                                                  | 
| 1  | cried is himself give me my head then the king                | brought two far in the window and the man came with pale and diamonds equipped a thousand folk this cages loudly and as he saw a white snake lying coiled                  | jug of them shining fast off behind him and raise the groom to his knees the white feather were lying on her head brought and saw over his head and said to him may do what she answered he speak hearing good fare watch and began to blaze the bird had stolen my ball nearer to it but how she had got into the horsemen and off there was no bridge like the might roll was very troublesome and there was so enough to hear that she was led to a troop of the church bell the giant came to them and everything to me else is done and then her mother knew nothing shall you be parted with them and child i will tell him up and make a slice of bread and they reward to and wanted to keep work at all it is and make care i shall be black dinner noise has done said she did how to give it on his neck and laughed when she had fallen upon the ground the judge persons were forced to speak but the work lay open the fire and did not believe them as she was freed about                                                                  | 
| 2  | kitchen and shook out the willowwren flew up to his           | has supported me down into the cellar and see where my father grieved when we to eat of the sexton came to the door he leapt into the inn there                            | natural shapes again and all she stopped to eat and were dead a single bird who was very long and they called out which was a gentle has so long a shoemaker was a boy went into her chamber and played on her fiddle and asked her many clothes and did not succeed and feel away and you may even shall not conceive what big you give me the four things for chanticleer witch shall soon find the door of the land they might sleep at length she came to the seashore and the riches shone through the moonlight standing into the water where he went home again and the princess said to the peasant bid him by face shall it give me you to the riches then the peasant trustfully the boy you led him cut her and round and the old king saw what was all very hard and would have learnt what he was over and dishes to open the miller and he set them free and begged the same deer that he asked what was the matter it was standing outside her guard and went with the giant and took was leave or eight she saw                            | 
| 3  | foot and limped hobblety jib hobblety and when he came        | him joy at once the king had a great thirst and mother so she sat down by the fields and then he ran back to her grave and said what                                       | let nothing do you kept your claws said the king has to do what my but place and yet i must give me their tobacco third time he gave it some one hans came to her and the other hair and kicked how of ever brought a light which ailed her service for water from two lodging and after them herself grieved it but the eldest son lived thinking that the wheels might as the peasants was obliged to keep his daughter ilsabill came in and sat by the inn and upon if she were journeying thither else and noticed a great thirst and said whether he has my life well for you as well as if i have said the miller is in doing saying you will hold the two eldest should not conceive than the countryman made his tobacco pipe and went with along his wings and catherine lived very fond of their wife and the water of the river the king and the people who was the cow and when he knew him out nevertheless he soon came to the castle lay a cow to the castle and then nestled in which it chanced to eat and                                | 
| 4  | and when he had gone on her she walked out                    | dead an old fox too for she began to bewail them began with gold and sleep dogs yet fiddle and then her mother should find him as he could even                            | before then she gave him him with a time and then an door did how trees again over the furskin claw and said quite yourselves back on the roof and took it in heaven and shut the lid then she saw their heads and brought all them home again and marleen still standing in his hand and squeezed it at her and not any upstairs towards all this too thinking that they were all sitting with their entreaties as he was able to try and kept sighed the little man with it and said is all my the second sister is to be godmother he says a little creature should have a dainty noise and said you may not believe the corn and he did not get the best of his friends and next rock bade him make the truth and the shepherd met them running too dress and said will be an hard now as the as he did not come back to blow though he made his consent and went upon the skin and carried the pan without two daughters a good time knocked at the door now when he came to the castle he stood forced out                                           | 
| 5  | place and when he saw the bridegroom screamed out and         | after something but that you can have my thirst but happen to said the youth and was travelling dead cup to the bottom of the movements door remained a raven              | changed into a bird and had not been a fool him which his wife stretched up his eyes but when she had run into the night when at the house he went asleep and the king had heard a troop of nutshells and when she came to the ground had a little way over the crowd for each dress but the cook said to the second place now he carries a cow and stoop so that my father has got the bird standing in a deep sleep so big for the princess and be sure to the giant however had heard but she went inside looked in a tree and beaten him into the forest but a small brook and when he had fastened that the others had given out the goat made her and caused a little invisible behind his hand think he had been mocking it and the cock showed him out again in the path was sent and she was calling on his way to ask how to have any luck that the poor days accomplished and she sent it to the sparrow in the street and saw how she had bound up together lay full of                                                                                                           | 

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
        type = list,
        default = [128, 100],
        required = False,
        help = "list of integers - specifying number and depth of LTSM layers")
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

