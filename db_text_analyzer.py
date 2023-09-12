import numpy as np
import codecs

from text_analyser import TextAnalyser
from db_text_data_extractor import DBTextDataExtractor
from DAO_TP2 import DAO

class DBTextAnalyzer(TextAnalyser):
    
    def __init__(self, cmws=None):
        super().__init__(cmws= cmws)
        self.dao = DAO()
        
    def pull_database_data(self):
        self.pull_database_words()
        self.pull_database_comatrix()
        
    def pull_database_words(self):
        self.word_dict = self.dao.get_words_dict()
    
    def pull_database_comatrix(self):
        co_matrix_datapoints = self.dao.get_cooccurrences_matrix_datapoints(self.co_matrix_window_size)
        self.co_matrix = np.zeros((len(self.word_dict), len(self.word_dict)))
        for row, col, value in co_matrix_datapoints:
            self.co_matrix[row-1, col-1] = value
        
    def pull_text_stopwords(self, text_path, encoding_type):
        with codecs.open(text_path, "r", encoding_type) as f:
            return f.read()
        
    def unshift_word_dict(self):
        self.word_dict = {word: index - 1 for word, index in self.word_dict.items()}
        
if __name__ == '__main__':
    cmws = 5
    dbta = DBTextAnalyzer(cmws)
    dbta.stopwords = dbta.pull_text_stopwords("C62\Docs\stop_words.txt", "utf-8").split()
    
    dbta.dao.connect()
    dbta.pull_database_data()
    dbta.unshift_word_dict()
    # dbta.dao.reset_database()
    
    
    synonyms, score= dbta.evaluate_synonyms('bras', 12, 2)
    for synonym, score in zip(synonyms, score):
        print(synonym + " ----> " + str(score))  
                  