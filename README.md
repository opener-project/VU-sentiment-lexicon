VU-sentiment-lexicon
====================

This is a library to load and query sentiment lexicons in English, Dutch, German, Italian, Spanish and French. This library is required to use other components like the VU-polarity-tagger or
the VU-sentiment-aggregator.

The first thing you need is to clone the github repository:

````shell
git clone git@github.com:opener-project/VU-sentiment-lexicon.git
````

There are two ways of install the library.

Configuration
-------------
This is the easiest way to use the library and make it available to the rest of modules. The only requirement is
to include the folder where you did the clone of the repository in your PYTHONPATH envinronment variable



Installation
------------
Once you have all the files, you have to install the python library so that you can use it from other
python modules and script. For this purpose we provide an script called setup.py. To install the library:

````shell
python setup.py install
````

This command will install the VUSentimentLexicon. In some cases and depending on your system, you need root
permissions to perform this action. In case you have no permisions to write in the python libraries folder
or if you want to install this library in another folder, you can use the --prefix option.

````shell
python setup.py install --prefix=your_selected_path
````

In this case you should modify the PYTHON_PATH envinroment variable to include the folder where you installed the
library so that python could find the library. Depending on your system, the structure of the folder can be different.
If you use linux or MAC the folder you have to add to your PYTHON_PATH is your_selected_path/lib/pythonX.Y/site-packages
If you use windows: prefix\Lib\site-packages

Including new lexicons
----------------------
New lexicons can be included. They need to follow the proper OpeNER-LMF format (xml based). To do this, you have to copy
the new lexicon (my_new_lex.xml) into the correct folder for your language (for instance, for English in `VU-sentiment-lexicon/VUSentimentLexicon/EN-lexicon`).
Then you will need to modify the config.xml file under the same folder. This file contains the information and metadata about the available lexicons, and
include the information about the new one:
1) identifier: will be used to refer to this lexicon
2) description of the new lexicon
3) filename (my_new_lex.xml)
4) resource: the resource from which it has been created

For our new lexicon, we should create a new XML element "lexicon" like this:
````shell
  <lexicon id="own_lexicon" default="1">
    <filename>my_new_lex.ml</filename>
    <description>This is the new lexicon created with the double propagation algorithm</description>
    <resource>Opener annotated data</resource>
  </lexicon>
````
With this code in the config.xml the new lexicon will be available using the identifier "own_lexicon". With the option `default="1"` you will
make it the default one loaded by the library if no lexicon identifier is provided. Do not modify the name of the file config.xml and do not
remove any previous content unless you want to remove any available lexicon from the list.


French lexicon
--------------

There are two lexicon:

1) fr-sentiment_lexicon-old.lmf: lexicon generated following the propagation algorithm.

2) fr-sentiment_lexicon.lmf: the new lexicon.

The new one has been built as described below:

The method is based on SentiWordNet and basically we map, SentiWorNet to the WOLF synsets. We calculate a score with them:

  1 - positive_polarity - negative_polarity

1) Filter the result synsets depending on the Part of Speech:

  Nouns: if polarity is higher than 0.5 (positive or negative) => include.

  Verbs: if polarity is higher than 0.5 (positive or negative) => include.

  Adverbs: if polarity is higher than 0.5 (positive or negative) => include.

  Adjectives: include all of them.
 
2) Correct polarity with the french 1000 more frequent words file.

3) Build a csv file, then we build the lmf file with ruben's script from VUA (activate -verbose option), and we add the intensifiers/weakeners/polarityShifters.

4) Annotate polarity of 10 files with the VU-polarity-tagger.

5) Manually correct lexicon with the most common errors (stop words, neutral verbs, etc). Keep in mind that the polarity tagger does not use WSD, only lemmatization and Part of Speech, so we do the corrections in that direction.

Reference
----------
Maks I, Izquierdo R, Frontini F, Agerri R, Vossen P (2014) Generating polarity
lexicons with wordnet propagation in five languages. In: Proceedings of the Ninth
International Conference on Language Resources and Evaluation (LREC'14)

Contact
----------
* Ruben Izquierdo
* Vrije University of Amsterdam
* ruben.izquierdobevia@vu.nl

(Last update 4th-Mar-2014)
