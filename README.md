VU-sentiment-lexicon
====================

This is a library to load and query sentiment lexicons in English, Dutch and German. This library is required to use other components like the VU-polarity-tagger or
the VU-sentiment-aggregator.

The first thing you need is to clone the github repository:

````shell
git clone git@github.com:opener-project/VU-kaf-parser.git
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

