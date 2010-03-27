import Language
import Database.Database
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
                    meaning TEXT);''',
                '''CREATE TABLE IF NOT EXISTS kanji
                    (id INTEGER PRIMARY KEY,
                    kanji TEXT,
                    reading TEXT,
                    meaning TEXT,
                    kun_on TEXT);''',
                '''CREATE TABLE IF NOT EXISTS compounds
                    (id INTEGER PRIMARY KEY,
                    id_kanji INTEGER,
                    reading TEXT,
                    meaning TEXT,
                    kun_on TEXT);''',
                '''CREATE TABLE IF NOT EXISTS scorevocab
                    (id INTEGER,
                    user TEXT,
                    meaning_je INTEGER, 
                    meaning_ej INTEGER);''',
                '''CREATE TABLE IF NOT EXISTS scorekanji
                    (type TEXT,
                    id INTEGER,
                    user TEXT,
                    reading INTEGER, 
                    meaning INTEGER);''',
                '''CREATE TABLE IF NOT EXISTS scorecompounds
                    (type TEXT,
                    id INTEGER,
                    user TEXT,
                    reading INTEGER, 
                    meaning INTEGER);''',
                '''CREATE TABLE IF NOT EXISTS lists
                    (type TEXT,
                    id INTEGER
                    list TEXT
                    level INTEGER);''']
