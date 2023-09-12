# from sys import path

# path.append('..')

# path.append('../TP2/')

# path.append('../TP3/')

# from TP2.db_text_analyzer import DBTextAnalyzer

# from TP2.db_text_data_extractor import DBTextDataExtractor

# from TP2.DAO_TP2 import DAO

from KNN import KNN

from db_text_analyzer import DBTextAnalyzer

from db_text_data_extractor import DBTextDataExtractor

from DAO_TP2 import DAO

from msvcrt import getch


from tp3_argchecker import TP3ArgsChecker

from clusterer import Clusterer


import traceback
import codecs
import time



class App:

    def __init__(self):

        self.args = TP3ArgsChecker()


        self.args = self.args.get_args()


    def open_user_instructions(self):

        with codecs.open("./user_instructions.txt", "r", "utf-8") as f:

            contents = f.read()
        return contents


    def gotcha(self, prompt):
        print(prompt)

        try:

            input = getch().decode("utf-8")

        except:

            input = getch()
        return input


    def run(self):

        if self.args.t:

            if self.args.e:
                self.train()


            elif self.args.r:

                self.ta = DBTextAnalyzer(int(self.args.t))

                self.ta.stopwords = self.ta.pull_text_stopwords(

                    ".\stop_words.txt", "utf-8"
                ).split()

                self.search_synonyms()


            elif self.args.c:

                self.ta = DBTextAnalyzer(int(self.args.t))

                if self.args.knn:

                    options = {}

                    if self.args.ponderation:

                        options["ponderation"] = self.args.ponderation

                    if self.args.normaliser:

                        options["normaliser"] = self.args.normaliser

                    self.knn = KNN(self.args.knn, ponderation=self.args.ponderation, normaliser=self.args.normaliser)

                self.ta.stopwords = []

                self.cluster_words()


        elif self.args.b:

            self.reinitialize_database()


    def print_prologue(self):

        for _ in range(4):
            print()
        print(

            "Cette application sert à trouver des synonymes d'un mot donné dans un texte donné. Elle utilise une matrice de co-occurrence pour trouver les synonymes les plus proches du mot donné."
        )
        print()

        print("Caractéristiques: ")
        print()
        print(

            "- Taille de fenêtre d'observation de la matrice de co-occurrence: "

            + self.args.t

            + " *"
        )
        print()
        print(

            "* De chaque côté du mot central, il y a (n-1)/2 mots analysés, où n est la taille de la fenêtre d'observation."
        )
        print()
        print()


    def print_epilogue(self):
        print(

            "Hearken! The hour of departing draweth nigh, fair gents. Hence, it is with a melancholy spirit that I bid thee farewell, forsooth. May the divine holys bestow upon thee abundant blessings and direct thee on thy sojourn, until our paths crosseth anew."
        )
        print()
        print(

            "Réalisé par Jonathan Robison-Roberge et Andrzej Wisniowski. ChatGPT et CoPilot ont été utilisés pour bonifier ce travail."
        )


    def train(self):

        if self.args.v:

            print("Évaluation du texte en cours, veuillez patienter...")

            start_time = time.perf_counter()

        try:

            db_data_extractor = DBTextDataExtractor(

                self.args.chemin, self.args.enc, int(self.args.t)
            )

            db_data_extractor.extract_words()

            db_data_extractor.dao.connect()

            db_data_extractor.reshift_word_dict()

            db_data_extractor.merge_word_dicts()

            db_data_extractor.export_word_dict_to_sqlite_db()

            db_data_extractor.unshift_word_dict()

            db_data_extractor.evaluate_ordered_cooccurrence_matrix()

            db_data_extractor.reshift_word_dict()

            db_data_extractor.export_ordered_cooccurrence_matrix_to_sqlite_db()

            db_data_extractor.extract_word_types_and_export_to_db("knn_prof\Lexique382.tsv", "\t", [0, 3, 8])


        # codiga-disable

        except Exception as e:

            traceback.print_exc()

        finally:

            db_data_extractor.dao.disconnect()


        if self.args.v:

            total_time = time.perf_counter() - start_time

            print(f"Évaluation du texte {self.args.chemin} terminée avec succès!")

            print("Temps d'exécution: " + str(round(total_time, 3)) + " secondes.\n")


    def evaluate_word_synonyms(self, user_input):

        queried_word = user_input[0]

        n_of_synonyms = int(user_input[1])

        operation_method_no = int(user_input[2])

        print("\nEn cours d'exécution, veuillez patienter...")


        if self.args.v:

            start_time = time.perf_counter()


        synonyms = None

        try:

            synonyms, scores = self.ta.evaluate_synonyms(

                queried_word, n_of_synonyms, operation_method_no
            )

            print("\nRésultats: \n")

            for synonym, score in zip(synonyms, scores):

                print(synonym + " ----> " + str(score))

            if self.args.v:

                total_time = time.perf_counter() - start_time
                print(

                    "\nMéthode d'opération: "

                    + str(

                        self.ta.synonym_finder_operations_dict[operation_method_no][

                            "name"

                        ]
                    )

                    + "."
                )
                print(

                    "Temps d'exécution: " + str(round(total_time, 3)) + " secondes.\n"
                )

        except Exception as e:
            print(e)


        user_input = self.gotcha(

            "Appuyez sur une touche pour recommencer ou q pour quitter."
        )
        return user_input


    def search_synonyms(self):

        user_input = None


        try:
            self.prepare_data()


            while user_input != "q":

                if self.args.v:

                    self.print_prologue()


                user_input = input(self.open_user_instructions()).split()


                if len(user_input) == 1 and user_input[0] == "q":

                    break

                elif len(user_input) == 3:

                    user_input = self.evaluate_word_synonyms(user_input)


        except Exception as e:

            traceback.print_exc()

        finally:
            self.ta.dao.disconnect()


        if self.args.v:

            self.print_epilogue()


    def reinitialize_database(self):

        if self.args.v:

            print("Réinitialisation, veuillez patienter...")

            start_time = time.perf_counter()

        try:

            dao = DAO()
            dao.connect()

            dao.reset_database()

        except Exception as e:

            traceback.print_exc()

        finally:
            dao.disconnect()

        if self.args.v:

            print("Réinitialisation terminée.")

            total_time = time.perf_counter() - start_time

            print("Temps d'exécution: " + str(round(total_time, 3)) + " secondes.\n")


    def cluster_words(self):

        try:
            self.prepare_data()
            
            

            self.clusterer = Clusterer(self.ta.co_matrix, self.args.k, self.args.v)

            clusters = self.clusterer.cluster()

            if self.args.v:

                for cluster in range(int(self.args.k)):

                    print("Pour le cluster " + str(cluster + 1) + ": ")

                    for word_index in range(int(self.args.n)):

                        length = len(clusters[cluster])

                        if word_index <= length - 1:

                            word_indexer = {

                                # +1 because the word_dict is 1-indexed

                                value + 1: key for key, value in self.ta.word_dict.items()

                            }

                    if self.args.knn:

                        self.knn.evaluate_labels(clusters[cluster])


        except Exception as e:

            traceback.print_exc()

        finally:
            self.ta.dao.disconnect()


        if self.args.v:

            self.print_epilogue()


    def prepare_data(self):
        self.ta.dao.connect()

        self.ta.pull_database_data()

        self.ta.unshift_word_dict()



def main():

    app = App()
    app.run()



if __name__ == "__main__":

    quit(main())

