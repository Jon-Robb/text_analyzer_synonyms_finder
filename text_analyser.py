import numpy as np

from text_data_extractor import TextDataExtractor

class TextAnalyser:
    def __init__(self, tde=None, cmws=None):
        self.synonym_finder_operations_dict = { 
                                    0: {
                                        'name': 'Produit scalaire',
                                        'method': self.evaluate_synonyms_by_scalar_product,
                                        'elimination': -1
                                        },
                                    1: {
                                        'name': 'Moindres carrés',
                                        'method': self.evaluate_synonyms_by_least_squares,
                                        'elimination': np.inf
                                        },
                                    2:  {
                                        'name': 'Distance de Manhattan',
                                        'method': self.evaluate_synonyms_by_cityblock,
                                        'elimination': np.inf
                                    }
                                }
        if tde:
            self.integrate_text_data(tde)
            self.stopwords = tde.extract_text("C62\Docs\stop_words.txt", "utf-8").split()

            
        self.check_co_matrix_window_size(cmws)
        self.co_matrix_window_size = cmws
        self.synonyms_dict = {}
        # self.stop_words = tde.extract_text("../Docs/stop_words.txt", "utf-8").split()
        
    def integrate_text_data(self, tde):
        self.text = tde.text
        self.words = tde.words
        self.word_dict = tde.word_dict
        self.n_unique_words = tde.n_unique_words
        self.co_matrix = tde.co_matrix
        
    def evaluate_synonyms_by_cityblock(self, co_matrix, co_vector):
        return np.sum(np.abs(co_matrix - co_vector), axis=1)
    
    def evaluate_synonyms_by_least_squares(self, co_matrix, co_vector):
        return np.sum((co_matrix - co_vector)**2, axis=1)  
      
    def evaluate_synonyms_by_scalar_product(self, co_matrix, co_vector):
        return np.dot(co_matrix, co_vector)
        
    def evaluate_synonyms(self, queried_word, n_synonyms, operation_method_no):        
        if queried_word not in self.word_dict:
            return "The word you provided is not in the text. Please try again.\n", None
        elif n_synonyms > len(self.word_dict) - 1:
            return "You asked for more synonyms than there are words left in the text. Please try again.\n", None
        elif n_synonyms <= 0:
            return "You must provide a positive number of synonyms. Please try again.\n", None

        # codiga-disable
        else:
            word_index = self.word_dict[queried_word]
            stop_words_indices = [self.word_dict[word] for word in self.stopwords if word in self.word_dict]
            co_vector = self.co_matrix[word_index]
            
            # Use the appropriate method to evaluate scores.
            scores = self.synonym_finder_operations_dict[operation_method_no]['method'](self.co_matrix, co_vector)
            
            # Eliminate certain words (current word and stop words).
            scores[word_index] = self.synonym_finder_operations_dict[operation_method_no]['elimination']
            scores[stop_words_indices] = self.synonym_finder_operations_dict[operation_method_no]['elimination']

            # Transform OrderedDict to np.array.
            words = np.asarray(list(self.word_dict.keys()))
            
            # Sort by score as primary sort key, then words as secondary key. Use appropriate order according to evaluation method.
            sorted_indices = np.lexsort((words, -scores)) if operation_method_no == 0 else np.lexsort((words, scores))

            # Stack the arrays and sort them using the indices.
            stacked_mat = np.stack((words, scores), axis=1)
            sorted_stacked_mat = stacked_mat[sorted_indices]
            
            # Return the appropriate number of synonyms.
            return sorted_stacked_mat[:n_synonyms, 0], sorted_stacked_mat[:n_synonyms, 1]
            
            
    def check_co_matrix_window_size(self, cmws):
        if cmws % 2 == 0:
            raise ValueError("Window size must be odd.")

    def evaluate_ordered_cooccurrence_matrix(self):
        
        if not hasattr(self, 'words'):
            raise ValueError("You must first integrate the text data.")
        
        if not hasattr(self, 'co_matrix_window_size'):
            raise ValueError("You must first set the co-occurrence matrix window size.")
        
        co_matrix_half_window = (self.co_matrix_window_size - 1) // 2

        co_matrix = np.zeros((self.n_unique_words, self.n_unique_words))
        
        for i, word in enumerate(self.words):
            start, end = max(0, i - co_matrix_half_window), min(len(self.words), i + co_matrix_half_window + 1)
            co_words = np.array([self.word_dict[w] for j, w in enumerate(self.words[start:end]) if j != min(i, co_matrix_half_window)])
            np.add.at(co_matrix[self.word_dict[word]], co_words, 1)
            
        self.co_matrix = co_matrix

def main():
    tde = TextDataExtractor("C62/Docs/DummyTextUTF8.txt", "utf-8")
    ta = TextAnalyser(tde, 3)
    synonyms, scores = ta.evaluate_synonyms('d', 3, 0)
    for synonym, score in zip(synonyms, scores):
        print(synonym + " ----> " + str(score))  
                  
if __name__ == "__main__":
    quit(main())