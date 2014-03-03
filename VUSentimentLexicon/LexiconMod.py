import sys
import codecs
import logging
import os
import re
from collections import defaultdict
from lxml import etree


#####################
# Changes:
# 20-dic-2012: new hotel lexicons from Isa updated
#########


class LexiconSent:

    def __init__(self,language='nl',lexicon_id=None):
        self.VERSION = '1.0'
        logging.debug('Loading lexicon for '+language)
        self.__module_dir = os.path.dirname(__file__)
        self.sentLex = {}
        self.negators = set()
        self.intensifiers = set()        
        #self.posOrderIfNone = 'nvar'  ##Order of pos to lookup in case there is Pos in the KAF file
        self.posOrderIfNone = 'NRVGA'
        self.resource = "unknown"
        
        self.load_resources(language,lexicon_id)

        '''        
        if language == 'nl':
            self.load_resources()
            self.filename = os.path.join(self.__module_dir,'NL-lexicon','Sentiment-Dutch-HotelDomain.xml') ## Domain specific
            self.resource = 'VUA_olery_lexicon_nl_lmf'
        elif language == 'en':
            self.filename = os.path.join(self.__module_dir,'EN-lexicon','Sentiment-English-HotelDomain.xml')
            self.resource =  'VUA_olery_lexicon_en_lmf'
        elif language == 'de':
          self.filename = os.path.join(self.__module_dir,'DE-lexicon','Sentiment-German-HotelDomain.xml')
          self.resource =  'VUA_olery_lexicon_de_lmf'
        elif language == 'fr':
          self.filename = os.path.join(self.__module_dir,'FR-lexicon','fr-sentiment_lexicon.lmf')
          self.resource = 'Vicomtech_general_lexicon_french'
        elif language == 'it':
          self.filename = os.path.join(self.__module_dir,'IT-lexicon','it-sentiment_lexicon.lmf')
          self.resource = 'CRN_general_lexicon_italian'
        elif language == 'es':
          self.filename = os.path.join(self.__module_dir,'ES-lexicon','es-sentiment_lexicon.lmf')
          self.resource = 'EHU_general_lexicon_spanish'
        else:
          print 'Language resource not available for ',language
          sys.exit(-1)
        '''  
                
        self.__load_lexicon_xml()


    def load_resources(self,language,my_id=None):
        folder_per_lang = {}
        folder_per_lang['nl'] = 'NL-lexicon'
        folder_per_lang['en'] = 'EN-lexicon'
        folder_per_lang['de'] = 'DE-lexicon'
        folder_per_lang['fr'] = 'FR-lexicon'
        folder_per_lang['it'] = 'IT-lexicon'
        folder_per_lang['es'] = 'ES-lexicon'
        
        config_file = os.path.join(self.__module_dir,folder_per_lang[language],'config.xml')
        lexicons_obj = etree.parse(config_file)
        lexicons = {}
        default_id = None
        first_id = None
        for lexicon in lexicons_obj.findall('lexicon'):
            this_id = lexicon.get('id')
            if first_id is None: first_id = this_id
            default = (lexicon.get('default','0') == '1')
            if default_id is None and default:
                default_id = this_id
            filename = lexicon.find('filename').text
            description = lexicon.find('description').text
            resource = lexicon.find('resource').text
            lexicons[this_id] = (filename,description,resource)
        if default_id is None: default_id = first_id
        
        id_to_load = None
        if my_id is None:
            id_to_load = default_id
        else:
            if my_id in lexicon:
                id_to_load = my_id
            else:
                id_to_load = default_id
                
        self.filename = os.path.join(self.__module_dir,folder_per_lang[language],lexicons[id_to_load][0])
        self.resource = lexicons[id_to_load][1]+" . "+lexicons[id_to_load][2]
        
            
            
        
        
    def getResource(self):
        return self.resource
    

    def convert_pos_to_kaf(self,pos):
        my_map = {}
        my_map['adj'] = 'G'
        my_map['adv'] =  'A'
        my_map['multi_word_expression']= 'O'
        my_map['noun']= 'N'
        my_map['other']= 'O'
        my_map['prep']= 'P'
        my_map['verb']= 'V'
        return my_map.get(pos.lower(),'O')

    
    def __load_lexicon_xml(self):
        logging.debug('Loading lexicon from the file'+self.filename)
        from collections import defaultdict
        d = defaultdict(int)
        tree = etree.parse(self.filename)
        for element in tree.getroot().findall('Lexicon/LexicalEntry'):
            id = element.get('id','')
            pos = element.get('partOfSpeech','')
            type=element.get('type','')
            short_pos = self.convert_pos_to_kaf(pos)
            
            type = element.get('type','')
            d[type]+=1
            lemma_ele = element.findall('Lemma')[0]
            lemma = ''
            if lemma_ele is not None:
                lemma = lemma_ele.get('writtenForm')
            
            sent_ele = element.findall('Sense/Sentiment')[0]
            polarity = strength = ''
            if sent_ele is not None:
                #print sent_ele
                polarity = sent_ele.get('polarity','')
                strength = sent_ele.get('strength','')
                
            if lemma!='':
                if type!='':
                    if type == 'polarityShifter':
                        #self.negators.add((lemma,short_pos))
                        self.negators.add(lemma)
                    elif type == 'intensifier':
                        self.intensifiers.add(lemma)
                elif polarity!='':
                    self.sentLex[(lemma,short_pos)]=polarity
                    ##print>>sys.stderr,lemma,short_pos,polarity
                    
        logging.debug('Loaded: '+str(len(self.negators))+' negators')
        logging.debug('Loaded: '+str(len(self.intensifiers))+' intensifiers')
        logging.debug('Loaded: '+str(len(self.sentLex))+' elements with polarity')
        
 
    
    def isIntensifier(self,lemma):
        return lemma in self.intensifiers
        
    
    def isNegator(self,lemma):
      return lemma in self.negators
      
    
    def getPolarity(self,lemma,pos):
      if pos:
          return self.sentLex.get((lemma,pos),'unknown'),pos
      else:
        for newpos in self.posOrderIfNone:
            if (lemma,newpos) in self.sentLex:
                logging.debug('Found polarify for '+lemma+' with PoS '+newpos)
                return self.sentLex[(lemma,newpos)],newpos
        return ('unknown','unknown')
    
    def getLemmas(self):
        for (lemma,pos) in self.sentLex: yield (lemma,pos)

      
      
                                        
                                
        
