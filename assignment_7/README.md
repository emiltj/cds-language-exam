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
| 15 | cried out because i should have no good and when              | that he went on and took a hatchet and ate before her and complained that day was a wonderful mountain wretch that he found a hair looking down but the                    | 
| 16 | bring out the most beautiful day there and said her           | to the castle of their palace or she went once over the way and to the little tailor how he had no heads hour wretch happy get rid of him                                  | 
| 17 | and haughty and conceited that care not drop and going        | presents my own and i will come back to me indeed not turn with you so weigh them badly said the boy but you shall let him thatsome wretch enough                          | 
| 18 | a special dwelling was assigned him the soldiers however were | since the moon however was angels of fire and said will sew big and was to be expected and come then the east peeped up to her own room and                                | 
| 19 | went a horse on his tail and the miller said                  | slipped out and cried you will do the water of life so he said to the shepherd knocked at the door and thought to himself you have cooked it but                           | 
| 20 | search of wood said he has fallen asleep and will             | asked him what he should get with the little tailor however were sitting behind a fire in order to have no purpose without be your husband said me i have                  | 
| 21 | gone seeking two soul princess who started and said you       | to the roof and the king was not living carried to dry away on his knees from his chamber and at last however his father asked gretel really sadly would                   | 
| 22 | thorns to seek that the judge replied his wife will           | in danger of fur ravens why are you meddling and go in and the bird knew no what a second in good kinds of mankind this time yet to fight                                  | 
| 23 | roof of which it was curdken once everything the old          | amazed you my wish to grant me he glared by the roof but went into her bosom came into her stomach passed into the stream and forgot the prince called                     | 
| 24 | over me and took my bones that they might lie                 | tree and as she said to him is not heavy for these a plank in bridge far that they know what could i have had said the fish in the                                         | 
| 25 | a faithful in a cage frightened the smell of the              | my then there was great rejoicing and the farmer often started with it the fox however came from herself into the kitchen for which the king had brought with her          | 
| 26 | cold and to work to thee you but i shall                      | does not swallow that rattled the door knowing alas if it is a quarter of the window the bird said has just to herself and hungry or i will give                           | 
| 27 | then he went to bed after that was left and                   | asked but yourself was baked through the trees but the princess drew out threepence called his cheeks the giant begged and the king took her and tapped his wedding behind | 
| 28 | has settled two servants and steal will make me dresses       | said am fond of butter and that you will not give me three luck there stay said the man your father and will perhaps raise on the same road forth                          | 
| 29 | what of your geese you will give you my daughter              | said the little tailor do you yet i will eat anything why the old king said wish you do something more we want to look at the fish and heaven                              | 
| 30 | see things this continued deer might will be said the         | together so quickly to her glass of his following horse again much in great pair of the wind and when he was so good and she was not at home                               | 
| 31 | you see the sun he gave it something and chanticleer          | of their fiery eyes he began to snuff through the rapidity that was a very good one again to the sake time the dwarf thought of it striding young redcap                   | 
| 32 | two bride but would not see no wicked things you              | of wishing and i am to anyone who does unless you wicked friend i have had the confidential task came he did not come back however they might be very                      | 
| 33 | that many things truly wished by many years and at            | him and so she went and cut off a blow and hung the silken by the coachhouse chanticleer put the blue beast round out his horse asked him whether of                       | 
| 34 | coming now put it down again at once the thieves              | so she took stock the spit and attendants in the crowd chattering off and said ha him is again in vain that you is three hard and to feed if                               | 
| 35 | him she saw that the task shall sometimes more haughtily      | were found to be the remembrance of a hair which the king closed and said want it is the matter and say have my holiness my and trample my strangers                       | 
| 36 | at last the little princess prayed will talk her when         | that was celebrated and all the land to whom the miser upstairs began to fire and when he had gone but the king saw lord that he had walked for                            | 
| 37 | should come swimming at her the kingdom has carried into      | till he had that one wished and walked up their shoes and dragged on cakes and he shot them over her and thought of them mrs fox my treasures spring                       | 
| 38 | any then the wolf ran home in the courtyard and               | the little beasts said to the miller were close then she went to sleep again and when he came to the third castle he called out this household if of                       | 
| 39 | the prisoner clung to the table and when the peasant          | on two and the other fur knew a great thing standing in the fire and did her more words and said of length when he came towards the tree to                                | 
| 40 | began to wander so fast that the blood ran out                | want to have a one seen than cannot work let me open the peasant and said may go into the cellar and be rowing with it and have asked me                                   | 
| 41 | the floor and he offered a bird for red as                    | you to work said the king said to the shepherd riding will be a pioneer for this time and a waggoner as iron as you will not have another riches                           | 
| 42 | the air flying slowly round and the horse scrambled merrily   | she was forced to put a heads in great face and a while he gave her a piece of wood suddenly after that land seeking two to live in and                                    | 
| 43 | cannot will keep you tonight that you will give thee          | the old king did not know what to pay for his comrade by the princesses said to the giant you may have a charm for the glass of the youth                                  | 
| 44 | could no longer prevent all his money was sure that           | with it but the princess find upstairs as before the mayor who must be sit in your head cannot reach on the steps but not and when promise to plant                        | 
| 45 | husband then the fox came and said am the said                | merrily by them and the cock came and the king who was very tired she took their den her deliverer who had been forced to take a stones that dragging                      | 
| 46 | his mouth and cried out shall shake me give you               | married tom began to serve on her and took the lid heart was play in two then he took her time from her head and after it was near she                                     | 
| 47 | he went out and said must not give so the                     | let them do what the fox were angels with its lips and binds up her skin and his constable and paid that revived so while the cock agreed to have                          | 
| 48 | or what a costly grasshopper merchant is here and yet         | see that the work was quite granted but when she saw a large grasshopper sun he gave her a little hind too gift was a road outside her way had                             | 
| 49 | when he got up the cock hands and said are                    | and wonderful as big cannot make you asked to have your the other another discovered in manner of but the king had been afraid that was not one of a                       | 


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

