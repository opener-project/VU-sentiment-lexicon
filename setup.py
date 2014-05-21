from distutils.core import setup

setup(name='VUSentimentLexicon',
      version='1.1',
      description = 'Library in python to load and query sentiment lexicons',
      author = 'Ruben Izquierdo',
      author_email = 'r.izquierdobevia@vu.nl',
      packages = ['VUSentimentLexicon'],
      package_data = {'VUSentimentLexicon':['*-lexicon/*']}
      )
      
