DB_PATH = 'tp3.db'

FOREIGN_KEYS = 'PRAGMA foreign_keys = 1'

CREATE_TABLE_WORD = '''CREATE TABLE IF NOT EXISTS word 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    letters CHAR(128) UNIQUE NOT NULL,
    word_type CHAR(64) DEFAULT NULL
)
'''
CREATE_TABLE_COOCCURRENCE = '''CREATE TABLE IF NOT EXISTS cooccurrence
(
    window_size INTEGER NOT NULL,
    id_word INTEGER NOT NULL,
    id_coword INTEGER NOT NULL,
    count INTEGER NOT NULL,
    PRIMARY KEY (window_size, id_word, id_coword)
)
'''

DELETE_WORD_FROM_LETTERS = '''DELETE FROM word WHERE letters = ?'''

DELETE_LETTERS_FROM_ID = '''DELETE FROM word WHERE id = ?'''

DROP_TABLE_WORD = 'DROP TABLE IF EXISTS word'
DROP_TABLE_COOCCURRENCE = 'DROP TABLE IF EXISTS cooccurrence'

INSERT_WORD = '''INSERT INTO word (letters) VALUES (?)'''
INSERT_COOCCURRENCE = '''INSERT INTO cooccurrence (window_size, id_word, id_coword, count) VALUES (?, ?, ?, ?)'''

SELECT_WORD = '''SELECT letters, id FROM word'''
SELECT_COOCCURRENCE = '''SELECT * FROM cooccurrence WHERE window_size = ? AND id_word = ? AND id_coword = ?'''
SELECT_ALL_COOCCURRENCE = '''SELECT id_word, id_coword, count FROM cooccurrence WHERE window_size = ?'''
SELECT_WORD_AND_TYPE = '''SELECT id, word_type FROM word '''

UPDATE_WORD = '''UPDATE word SET letters = ? WHERE id = ?'''
UPDATE_COOCCURRENCE = '''UPDATE cooccurrence SET 
window_size = ?,
id_word = ?,
id_coword = ?,
count = ?
WHERE id = ?'''

UPSERT_COOCCURRENCE = '''INSERT INTO cooccurrence (window_size, id_word, id_coword, count) VALUES (?, ?, ?, ?) ON CONFLICT (window_size, id_word, id_coword) DO UPDATE SET count = count + ?'''

UPDATE_COOCCURRENCE_COUNT = '''UPDATE cooccurrence SET 
count = count + ?
WHERE window_size = ? AND id_word = ? AND id_coword = ?'''

UPDATE_OR_IGNORE_WORD_TYPE = '''UPDATE word SET word_type = ? WHERE letters = ?'''

