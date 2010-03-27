import Language
import Database.Database
from Language import RehearseTuple

class Korean():
    def __init__(self):
        pass
    database = "korean.db"
    name = "Korean"
    rehearse_types = [RehearseTuple("Vocabulary", "English Meaning", "vocab", "scorevocab")]
    tables_sql = ['''CREATE TABLE IF NOT EXISTS vocab    
                    (id INTEGER PRIMARY KEY,
                    r_ele TEXT,
                    k_ele TEXT,
                    meaning TEXT);''',
                '''CREATE TABLE IF NOT EXISTS scorevocab
                    (id INTEGER,
                    user TEXT,
                    meaning_je INTEGER, 
                    meaning_ej INTEGER);''',
                '''CREATE TABLE IF NOT EXISTS lists
                    (type TEXT,
                    id INTEGER
                    list TEXT
                    level INTEGER);''']
