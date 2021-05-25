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

This assignment seeks to generative new textual content by implementing a Recurrent Neural Network (RNN). More specifically, this assignment seeks see whether it is possible to generate new textual content in line with the text from [the corpus](https://www.kaggle.com/tschomacker/grimms-fairy-tales) of folklore fairytales written by the Brothers Grimm (Jacob Ludwig Karl Grimm and Wilhelm Carl Grimm). The project intends to investigate the questions: _How well can a neural network learn the patterns of the writings of the Brothers Grimm?_ and _Using the trained model - is it possible to generate new textual content that could have been something you read in an old fairytale?_.

Try using a text generative approach that learns and predicts on word-level, rather than on a character-level.

* Train a Long Short-Term Memory (LTSM) artificial Recurrent Neural Network (RNN) on the corpus
* Use sequences of 50 words as input for the model
* Bonus task: include arguments that let you specify model training parameters and LTSM model architecture (LTSM layers, epochs and batch size)
* Bonus task: include arguments that let you specify options for the generated texts. How many text chunks should be generated? What should be the length of the text chunks?

<!-- METHODS -->
## Methods

**Specifically for this assignment:**

For this assignment I started out by loading in the text corpus. The text was then preprocessed; all strings were appended to one long string. I tokenized the data up into the individual words, removed all non-alphanumeric characters and vectorized the data - having the text as integers instead of as strings to allow the model to train on the data. I defined and made use of a function retrieves word sequences using a moving window (e.g. ["once", "upon", "a", "time", "in"] becomes the sequences: [["once upon a"], ["upon a time"], ["a time in"]] when using window size = 3 and step size = 1). I chose to retrieve sequences of size 51. These first 50 tokens in each sequence would be used as features for the model input, while the last token in the sequence would be what the model tries to predict. The list of tokens to predict are then one-hot encoded to match the shape for a keras model that uses categorical crossentropy as loss function and softmax activation for the final layer.

<p align="center">
<a href="https://github.com/emiltj/cds-language-exam/README_images/text_generation_pipeline.png">
<img src="../README_images/text_generation_pipeline.png" alt="Logo" width="538" height="296">
</a>

<p align="center"><em>Visualization of the text generation pipeline utilized in the script</em></p>

The model consists of an embedding layer followed by two LTSM layers of depth 128 and 100 as per default. Using the argument --l, one may specify another structure for the LTSM layers, however. The model implements LTSM layers due to their way of handling the vanishing gradient problem (the problem of shrinking gradients over time in backpropagation), that is prevalent in traditional RNNs. It does so by the use of feedback connections called gates. The LTSM layers are succeeded by a dense layer (32 nodes) and an output layer that uses softmax and has the number of nodes equal to number of possible predictions.

The model is then trained on the data, learning the patterns in the sequences to be able to predict the next word in the sequence. Epochs and batchsize can be determines using the arguments (for more information, see section "Optional arguments").



<p align="center">
<a href="https://github.com/emiltj/cds-language-exam/README_images/text_generative_models.png">
<img src="../README_images/text_generative_models.png" alt="Logo" width="860" height="296">
</a>

<p align="center"><em>Visualization of the principle behind text generation algorithms. Image from blogpost by Harsh Basnal (https://bansalh944.medium.com/text-generation-using-lstm-b6ced8629b03) </em></p>

**On a more general level (this applies to all assignments):**

I have tried to as accessible and user-friendly as possible. This has been attempted by the use of:
* Smaller functions. These are intended to solve the sub-tasks of the assignment. This is meant to improve readability of the script, as well as simplifying the use of the script.
* Information prints. Information is printed to the terminal to allow the user to know what is being processed in the background
* Argparsing. Arguments that let the user determine the behaviour and paths of the script (see <a href="#optional-arguments">"Optional arguments"</a> section for more information)

<!-- RESULTS AND DISCUSSION -->
## Results and discussion

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
| 15 | cried out because i should have no good and when              | that he went on and took a hatchet and ate before her and complained that day was a wonderful mountain 

**Topic prevalence in schools of philosophical thought**
<p align="center">
<a href="https://github.com/emiltj/cds-language-exam/blob/main/assignment_5/out/plot_topic_prob.png"><img src="./out/plot_topic_prob.png" alt="Logo" width="1024" height="512">
<em> 
Plot showing the topic prevalence of the different schools of philosophical thought
</em>
</a>

When looking at the schools' topic prevalences the first thing that comes up is the high prevalence of topic 4 in the school of Aristotle. Topic 3 seems quite prevalent in books on Feminism, while Plato and Stoicms seems to be unrelated to most topics, say for topic 3.

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
        default = os.path.join("data", "philosophy_data.csv"), # Default path to data
        required = False,
        help= "str - path to image corpus")

<!-- CONTACT -->
## Contact

Feel free to write me, Emil Jessen for any questions.
You can do so on [Slack](https://app.slack.com/client/T01908QBS9X/D01A1LFRDE0) or on [Facebook](https://www.facebook.com/emil.t.jessen/).

