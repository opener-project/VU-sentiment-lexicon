import sys
import codecs
import logging
import os
import re
from collections import defaultdict

class LexiconSent:

    def __init__(self,language='nl'):
        self.logger = logging.getLogger('Basic_SA_system.LexiconSent')

        self.__module_dir = os.path.dirname(__file__)
        
        ## Internal variables
        self.wwVars = defaultdict(set)
        self.sentLex = {}
        self.negators = set()
        self.intensifiers = set()
        self.posOrderIfNone = 'nvar'  ##Order of pos to lookup in case there is Pos in the KAF file
        self.resource = "unknown"
        
        
        if language=='nl':
            self.__loadDutch()
            self.resource = 'VUA_polarity_lexicon_word_NL'
        elif language=='de':
            self.__loadGerman()
            self.resource = 'Zurich_polarity_lexicon_DE'
        elif language == 'en':
            self.__loadEnglish()
            self.resource = 'SubjectiveClues'
            
    def getResource(self):
        return self.resource
    
    def __loadEnglish(self):
        lexicon_file = os.path.join(self.__module_dir,'EN-lexicon','subjclueslen1-HLTEMNLP051.txt')
        try:
            my_re = re.compile(r'word1=([a-zA-Z0-9]+).*pos1=([a-zA-Z0-9]+).*priorpolarity=([a-zA-Z0-9]+)')
            fic = open(lexicon_file,'r')
            for line in fic:
                matches = my_re.findall(line)
                if len(matches) != 0 :
                    lemma,pos,polarity = matches[0]
                    if polarity in ['positive','negative','neutral']:
                      if pos=='anypos':
                        for my_pos in 'anrv':
                            self.sentLex[(lemma,my_pos)]=polarity
                      elif pos=='adverb':
                        self.sentLex[(lemma,'r')] = polarity
                      else:
                        self.sentLex[(lemma,pos[0])] = polarity
            fic.close()         
        except Exception as e:
            print str(e)
            
        ## Intensifiers
        for int in ['very','really','definetely','especially','seriously']:
            self.intensifiers.add(int)
        
        ## Negators
        for neg in ['no','not','never','none']:
            self.negators.add(neg)
        
            
    def __loadGerman(self):
        lexicon_file = os.path.join(self.__module_dir,'DE-lexicon','germanLex.txt')
        try:
            fic = codecs.open(lexicon_file,'r','utf-8')
            for line in fic:
                if line[0:2] != '%%':
                  fields = line.strip().split()
                  lemma = fields[0]
                  type, value = fields[1].lower().split('=')
                  pos = fields[2].lower()[0]
                 
                  
                  if type == 'pos':
                    self.sentLex[(lemma,pos)]='positive'
                  elif type == 'neg':
                    self.sentLex[(lemma,pos)]='negative'
                  elif type == 'neu':
                    self.sentLex[(lemma,pos)]='neutral'
                  elif type == 'int':
                    self.intensifiers.add(lemma)
                  elif type == 'shi':
                    self.negators.add(lemma)
                  else:
                    pass
            fic.close()
        except Exception as e:
            print str(e),line
        
            
        
    def __loadDutch(self):
        self.wwVarFile = os.path.join(self.__module_dir,'NL-lexicon','wwvars.txt')
        self.lexSentFile = os.path.join(self.__module_dir,'NL-lexicon','hotel-sentimentgi42.txt')     
        self.negatorsFile = os.path.join(self.__module_dir,'NL-lexicon','negators.txt')
        self.intensifiersFile = os.path.join(self.__module_dir,'NL-lexicon','intensifiers.txt')
 
        self.__loadLexWW()
        self.__loadLexSent()
        self.__loadNegators()
        self.__loadIntensifiers()    
        
    
    def __loadIntensifiers(self):
      try:
          f = open(self.intensifiersFile)
          for line in f:
            self.intensifiers.add(line.strip())
          self.logger.info('Loaded '+str(len(self.intensifiers))+' intensifiers')
          f.close()
      
      except Exception as e:
          self.logger.error(str(e))
    
    def isIntensifier(self,lemma):
        return lemma in self.intensifiers
        
    def __loadNegators(self):
      try:
          f = open(self.negatorsFile)
          for line in f:
            self.negators.add(line.strip())
          self.logger.info('Loaded '+str(len(self.negators))+' negators')
          f.close()
      
      except Exception as e:
          self.logger.error(str(e))
                                    
    
    def isNegator(self,lemma):
      return lemma in self.negators
      
      
    def __loadLexWW(self):
      try:
          #f = codecs.open(self.wwVarFile,'r','ISO 8859-1')
          f = open(self.wwVarFile)
          import HTMLParser
          h = HTMLParser.HTMLParser()
          for line in f:
            fields = line.strip().split('/')
            if len(fields)>2:
                for w in fields[1:]:
                    if w!='x':
                        self.wwVars[h.unescape(fields[0])].add(h.unescape(w))
          f.close()
          self.logger.info('Loaded '+str(len(self.wwVars))+' ww-vars')
      except Exception as e:
          self.logger.error(str(e))
  


    def __loadLexSent(self):
        n=ne=0
        try:
          f = open(self.lexSentFile)
          for line in f:
            fields = line.strip().split('/')
            lemma,pos,sent = fields[0:3]
            if pos=='adv':
                pos='r'
            self.sentLex[(lemma,pos)]=sent
            n+=1
            #print lemma,pos,sent
            for word in self.wwVars.get(lemma,[]):
              if word!='x':
                self.sentLex[(word,pos)]=sent
                ne+=1
                #print '\t',word,pos,sent
          f.close()
          self.logger.info('Number of words with sentiment from lexicon '+str(n))
          self.logger.info('Number of words with sentiment from wwVars '+str(ne))
        except Exception as e:
            self.logger.error(str(e))
            sys.exit(-1)
    
    def getPolarity(self,lemma,pos):
      if pos:
          return self.sentLex.get((lemma,pos),'unknown'),pos
      else:
        for newpos in self.posOrderIfNone:
            if (lemma,newpos) in self.sentLex:
                self.logger.info('Found polarify for '+lemma+' with PoS '+newpos)
                return self.sentLex[(lemma,newpos)],newpos
        return ('unknown','unknown')
    
    def getLemmas(self):
        for (lemma,pos) in self.sentLex: yield (lemma,pos)

      
      
                                        
                                
        
