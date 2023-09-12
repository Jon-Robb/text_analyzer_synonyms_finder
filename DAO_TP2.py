import sqlite3
import db_queries as dbq

class DAO:
    def __init__(self, path:str=dbq.DB_PATH):
        self.path = path
        
    def connect(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        self.cursor.execute(dbq.FOREIGN_KEYS)

    def disconnect(self):
        self.cursor.close()
        self.conn.close()
        
    def reset_database(self):
        self.flush_database()
        self.initialize_database()
        
    def initialize_database(self):
        self.cursor.execute(dbq.CREATE_TABLE_WORD)
        self.cursor.execute(dbq.CREATE_TABLE_COOCCURRENCE)
        self.conn.commit()

        
    def flush_database(self):
        self.cursor.execute(dbq.DROP_TABLE_COOCCURRENCE)
        self.cursor.execute(dbq.DROP_TABLE_WORD)
        self.conn.commit()

        
    def show_table(self, table, prompt):
        print(table)
        self.cursor.execute(prompt)
        for row in self.cursor.fetchall():
            print(row)
        
    def show_word(self):
        self.show_table('word', dbq.SELECT_WORD)
        
    def show_cooccurrence(self):
        self.show_table('cooccurrence', dbq.SELECT_COOCCURRENCE)
        
    def insert_word(self, word: str):
        self.cursor.execute(dbq.INSERT_WORD, (word,))
        self.conn.commit()
    
    def insert_words(self, list_letters:list):
        self.cursor.executemany(dbq.INSERT_WORD, [(w,) for w in list_letters])
        self.conn.commit()
        
    def insert_coocurrence(self, window_size: int, id_word1: int, id_word2: int):
        self.cursor.execute(dbq.INSERT_COOCCURRENCE, (window_size, id_word1, id_word2, 1))
        self.conn.commit()
    
    def update_cooccurrence_count(self, window_size: int, id_word1: int, id_word2: int, count:int):
        self.cursor.execute(dbq.UPDATE_COOCCURRENCE_COUNT, (count, window_size, id_word1, id_word2))
        self.conn.commit()
        
    def upsert_cooccurrence(self, window_size: int, id_word1: int, id_word2: int):
        self.cursor.execute(dbq.SELECT_COOCCURRENCE, (window_size, id_word1, id_word2))
        if self.cursor.fetchone() is None:
            self.insert_coocurrence(window_size, id_word1, id_word2)
        else:
            self.update_cooccurrence_count(window_size, id_word1, id_word2)

    def get_words_dict(self):
        self.cursor.execute(dbq.SELECT_WORD)
        result = dict(self.cursor.fetchall())
        return result
    
    def get_words_types(self):
        self.cursor.execute(dbq.SELECT_WORD_AND_TYPE)
        result = self.cursor.fetchall()
        result = {index: type for (index, type) in result}
        return result
    
    def get_cooccurrences_matrix_datapoints(self, window_size: int):
        self.cursor.execute(dbq.SELECT_ALL_COOCCURRENCE, (window_size,))
        return self.cursor.fetchall()
            
    def upsert_cooccurrences(self, list_tuples:list[tuple]):
        
        window_size = list_tuples[0][0]
        self.cursor.execute(dbq.SELECT_ALL_COOCCURRENCE, (window_size,))
        
        for cooccurrence in list_tuples:
            self.cursor.execute(dbq.UPSERT_COOCCURRENCE, (cooccurrence[0], cooccurrence[1], cooccurrence[2], cooccurrence[3], cooccurrence[3]))
        
        self.conn.commit()

    def upsert_word(self, word: str):
        self.cursor.execute(dbq.SELECT_WORD, (word,))
        if self.cursor.fetchone() is None:
            self.insert_word(word)
            
    def upsert_words(self, words: set):
        new_words = []
        self.cursor.execute(dbq.SELECT_WORD)
        words_in_db = [w[0] for w in self.cursor.fetchall()]
        for word in words:
            if word not in words_in_db:
                new_words.append(word)
        self.insert_words(new_words)
        
    def update_word_types(self, word_types: tuple):
        for word, type in word_types:
            self.cursor.execute(dbq.UPDATE_OR_IGNORE_WORD_TYPE, (type, word))
        self.conn.commit()
        
def insert_word_test(db):
    list = []
    for i in range(100):
        letters = 'mot' + str(i)
        list.append((letters,))
    db.insert_words(list)

    
def extract_unique_words(list):
    return set(list)
    
def test_upsert_words(db:DAO, list:list):
    db.upsert_words(list)
    
def test_upsert_cooccurrence(db, test_text):
    db.upsert_cooccurrence(test_text)
    
def test_insert_coocurrence(db):
    db.insert_coocurrence(1, 1, 2)

def main():
    
    test_text = 'Le chat est sur le tapis. Il mange une souris. La souris gémit. Le gémissement de la souris réveille le chat. Le chat se lève et court après la souris morte-vivante.'
    test_text = test_text.lower()
    test_text_set = set(test_text.split())
    # test_text = extract_unique_words(test_text)
    try :
        dao = DAO()
        dao.connect()
        #dao.reset_database()
        print('Database connected.')
        dao.get_words_dict()
                
        # Test your code here
        # test_upsert_words(dao, test_text_set)
        list_tuples = []
        for i in range(10):
            list_tuples.append((5, i, i+1, i+2))

        dao.upsert_cooccurrences(list_tuples)
        
        return 0
    
    except Exception as e:
        print(e)
        return 1
    
    finally:
        dao.disconnect()
        print('Database disconnected.')
    

if __name__ == "__main__":
    quit(main())