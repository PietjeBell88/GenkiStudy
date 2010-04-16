import Language
from Language import RehearseTuple

class Japanese():
    def __init__(self):
        pass
    
    database = "japanese.db"
    name = "Japanese"
    rehearse_types = [RehearseTuple("Vocabulary", "English Meaning", "vocab", "scorevocab"),
                      RehearseTuple("Kanji", "English Meaning", "kanji", "scorekanji"),
                      RehearseTuple("Compounds", "English Meaning", "compounds", "scorecompounds")]
    tables_sql = ['''CREATE TABLE IF NOT EXISTS vocab    
                    (id INTEGER PRIMARY KEY,
                    r_ele TEXT,
                    k_ele TEXT,
                    meaning TEXT,
                    UNIQUE(id, r_ele, k_ele, meaning));''',
                '''CREATE TABLE IF NOT EXISTS kanji
                    (id INTEGER PRIMARY KEY,
                    kanji TEXT,
                    reading TEXT,
                    meaning TEXT,
                    kun_on TEXT,
                    UNIQUE(id, kanji, reading, meaning, kun_on));''',
                '''CREATE TABLE IF NOT EXISTS compounds
                    (id INTEGER PRIMARY KEY,
                    id_kanji INTEGER,
                    reading TEXT,
                    meaning TEXT,
                    kun_on TEXT,
                    UNIQUE(id, id_kanji, reading, meaning, kun_on));''',
                '''CREATE TABLE IF NOT EXISTS scorevocab
                    (id INTEGER,
                    user TEXT,
                    meaning_je INTEGER, 
                    meaning_ej INTEGER,
                    UNIQUE(id, user));''',
                '''CREATE TABLE IF NOT EXISTS scorekanji
                    (id INTEGER,
                    user TEXT,
                    reading INTEGER, 
                    meaning INTEGER,
                    UNIQUE(id, user));''',
                '''CREATE TABLE IF NOT EXISTS scorecompounds
                    (id INTEGER,
                    user TEXT,
                    reading INTEGER, 
                    meaning INTEGER,
                    UNIQUE(id, user));''',
                '''CREATE TABLE IF NOT EXISTS lists
                    (type TEXT,
                    id INTEGER,
                    list TEXT,
                    level INTEGER,
                    UNIQUE(type, id, list, level));''']
