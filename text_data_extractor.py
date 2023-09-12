import codecs
from collections import OrderedDict
import re
import numpy as np

class TextDataExtractor:
    def __init__(self, text_path=None, encoding_type=None, window_size=None):
        if text_path and encoding_type:
            self.extract_text_data(text_path, encoding_type)
        elif not text_path and not encoding_type: pass
        else: raise ValueError("You must provide either both the text path and the encoding type or nothing at all.")
        self.co_matrix_window_size = window_size
        
    def extract_text_data(self, text_path, encoding_type):
        self.title = text_path.split('\\')[-1].split('.')[0].split('UTF8')[0]
        self.encoding_type = encoding_type
        self.text = self.extract_text(text_path, encoding_type)
        self.words = self.extract_words()
        self.word_dict = self.evaluate_word_dict()        
    
    def extract_text(self, text_path, encoding_type):
        with codecs.open(text_path, "r", encoding_type) as f:
            return f.read()
                
    def extract_words(self):
        no_punctuations_text = self.text
        punctuation_marks = ["'", '"', ',', '.', '!', '?', ';', '«', '»', '(', ')', '{', '}', '$', '_', '*', '-',':']
        for mark in punctuation_marks:
            no_punctuations_text = no_punctuations_text.replace(mark, " ")

        filtered_text = re.sub(r"[^\w\séèêëàäâùüûîïôöûœç]+|[0-9]+", ' ', no_punctuations_text, re.UNICODE)

        lowercase_filtered_text = filtered_text.lower()
        filtered_lowercase_words = lowercase_filtered_text.split()
        return filtered_lowercase_words
    
    def evaluate_word_dict(self):
        return OrderedDict((word, i) for i, word in enumerate(sorted(set(self.words))))

    def evaluate_ordered_cooccurrence_matrix(self):
        
        if not hasattr(self, 'words'):
            raise ValueError("You must first integrate the text data.")
        
        if not hasattr(self, 'co_matrix_window_size'):
            raise ValueError("You must first set the co-occurrence matrix window size.")
        
        co_matrix_half_window = (self.co_matrix_window_size - 1) // 2

        co_matrix = np.zeros((len(self.word_dict), len(self.word_dict)))
        
        for i, word in enumerate(self.words):
            start, end = max(0, i - co_matrix_half_window), min(len(self.words), i + co_matrix_half_window + 1)
            co_words = np.array([self.word_dict[w] for j, w in enumerate(self.words[start:end]) if j != min(i, co_matrix_half_window)])
            np.add.at(co_matrix[self.word_dict[word]], co_words, 1)
            
        self.co_matrix = co_matrix
        return co_matrix

    def remove_punctuation(text):
        for mark in punctuation_marks:
            text = text.replace(mark, " ")

        return text