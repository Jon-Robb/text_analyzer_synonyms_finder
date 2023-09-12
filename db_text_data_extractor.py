from text_data_extractor import TextDataExtractor

import numpy as np

from DAO_TP2 import DAO

import traceback



class DBTextDataExtractor(TextDataExtractor):

    def __init__(self, text_path=None, encoding_type=None, window_size=None):

        super().__init__(text_path, encoding_type, window_size)

        self.dao = DAO()


    def merge_word_dicts(self):

        dao_dict = self.dao.get_words_dict()

        self.evaluate_word_dict()

        for word in self.word_dict:

            if word not in dao_dict:

                dao_dict[word] = len(dao_dict) + 1

        self.word_dict = dao_dict


    def export_word_dict_to_sqlite_db(self):

        self.dao.upsert_words(self.word_dict.keys())


    def merge_cooccurrence_matrixes(self):

        dao_co_matrix_datapoints = self.dao.get_cooccurrences_matrix_datapoints(

            self.co_matrix_window_size
        )

        dao_co_matrix = np.zeros((len(self.word_dict), len(self.word_dict)))

        for row, col, value in dao_co_matrix_datapoints[1:3]:

            dao_co_matrix[row, col] = value

        # self.evaluate_ordered_cooccurrence_matrix()

        self.co_matrix += dao_co_matrix


    def export_ordered_cooccurrence_matrix_to_sqlite_db(self):

        ## add window size in the beginning of each tuple in the list

        co_matrix_datapoints = [
            (

                int(self.co_matrix_window_size),

                int(row) + 1,

                int(col) + 1,

                int(self.co_matrix[row, col]),
            )

            for row, col in np.argwhere(self.co_matrix > 0)

        ]


        self.dao.upsert_cooccurrences(co_matrix_datapoints)


    def unshift_word_dict(self):

        self.word_dict = {word: index - 1 for word, index in self.word_dict.items()}


    def reshift_word_dict(self):

        self.word_dict = {word: index + 1 for word, index in self.word_dict.items()}


    def extract_word_types_and_export_to_db(

        self, chemin: str, sep: str, columns_indices: list, enc="utf-8"

    ):

        word_types_dict = {}

        word_types_list = []

        with open(chemin, encoding=enc) as f:

            lines = f.read().splitlines()

            for line in lines:

                word_types_list.append([line.split(sep)[i] for i in columns_indices])


            for word, word_type, occurrence in word_types_list[1:]:

                if word in word_types_dict:

                    if float(occurrence) > float(word_types_dict[word][-1]):

                        word_types_dict[word] = (word_type, occurrence)

                else:

                    word_types_dict[word] = (word_type, occurrence)


            word_types_list = [

                (word, word_type) for word, (word_type, count) in word_types_dict.items()

            ]


        self.dao.update_word_types(word_types_list)
     


if __name__ == "__main__":

    try:

        db_data_extractor = DBTextDataExtractor("C62\Docs\GerminalUTF8.txt", "utf-8", 5)

        # db_data_extractor.extract_words()

        db_data_extractor.dao.connect()

        db_data_extractor.dao.reset_database()

        # db_data_extractor.reshift_word_dict()

        # db_data_extractor.merge_word_dicts()

        db_data_extractor.export_word_dict_to_sqlite_db()

        # db_data_extractor.unshift_word_dict()

        # db_data_extractor.evaluate_ordered_cooccurrence_matrix()

        # db_data_extractor.reshift_word_dict()

        # db_data_extractor.export_ordered_cooccurrence_matrix_to_sqlite_db()

        lexique = db_data_extractor.extract_word_types_and_export_to_db("C62\TP3\knn_prof\Lexique382.tsv", "\t", [0, 3, 9])

        db_data_extractor.add_word_types_to_db(lexique)


    except Exception as e:

        traceback.print_exc()

        # finally:

        db_data_extractor.dao.disconnect()

