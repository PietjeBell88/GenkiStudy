# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import re
import codecs
import sqlite3

class JMDict():
    def __init__(self,path,c):
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.c = c

    def insert_into_db(self):
        #entrylist = (entry for entry in self.root if (entry.find("ent_seq").text == "1010590"))
        entrylist = (entry for entry in self.root)
        for entry in entrylist: #(entry for entry in self.root if (entry.find("ent_seq").text == "1000000")):
            #Check to see if there are kanji elements. 
            #If there are, make a list of it
            #Else, make a list with one entry None so we can keep on looping.
            if len(entry.findall("k_ele")) == 0:
                keblist = [None]
            else:
                keblist = (k_ele.find("keb").text for k_ele in entry.findall("k_ele"))
            
            for keb in keblist:
                # Find all fitting reb's by looking for any "re_restr". It's a fitting one if:
                # 1: There is no re_restr in the r_ele
                # 2: The text value of the re_restr entry equals keb
                reblist = (r_ele.find("reb").text for r_ele in entry.findall("r_ele") if not [restr.text for restr in r_ele.findall("re_restr")] or keb in [restr.text for restr in r_ele.findall("re_restr")])
                        
                for reb in reblist:
                    print keb, reb
                    sql = "INSERT OR REPLACE INTO vocab_karo (k_ele, r_ele) VALUES (?,?);"
                    self.c.execute(sql, [keb, reb])

                    rowid = self.c.lastrowid
                    
                    # Every single gloss (in a "sense" entry) belongs to all the rebs/kebs, so no conditionals here.
                    # However, we don't want any foreign meanings, so the language has to be english (default).
                    for sense in entry.findall("sense"):

                        lastpos = None;
                        
                        stagk = sense.findall("stagk")
                        stagr = sense.findall("stagr")
                        
                        stagk = [stag.text for stag in stagk]
                        stagr = [stag.text for stag in stagr]

                        if (not stagk and not stagr) or (not stagk and reb in stagr) or (not stagr and keb in stagk):
                            for meaning in (gloss.text for gloss in sense.findall("gloss") if gloss.get("{http://www.w3.org/XML/1998/namespace}lang", "eng") == "eng"):
                                print rowid, meaning
                                sql = "INSERT OR REPLACE INTO vocab_meaning (karo_id, meaning) VALUES (?,?);"
                                self.c.execute(sql, [rowid, meaning])

                            if sense.findall("pos") is None:
                                newpos = lastpos
                            else:
                                newpos = [pos.text for pos in sense.findall("pos")]
                                lastpos = newpos;
                            for pos in newpos:
                                print rowid, pos
                                sql = "INSERT OR REPLACE INTO vocab_partofspeech (karo_id, pos) VALUES (?,?);"
                                self.c.execute(sql, [rowid, pos])
class KanjiDic2():
    def __init__(self,path,c):
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.c = c

    def insert_into_db(self):
        #entrylist = (entry for entry in self.root if (entry.find("ent_seq").text == "1010590"))
        entrylist = (entry for entry in self.root)# if entry.find("literal") is not None and entry.find("literal").text == "迪")
        for entry in entrylist: #(entry for entry in self.root if (entry.find("ent_seq").text == "1000000")):
            #Check to see if there are kanji elements.
            if entry.find("literal") is None:
                continue
            else:
                kanji = entry.find("literal").text
             
            # Get misc information (stroke_count, radical value..)
            stroke_count = int(entry.find("misc").find("stroke_count").text)
            rad_nelson_c = None
            rad_classical = None

            for bla in [rad_value for rad_value in entry.find("radical").findall("rad_value")]:
                if bla.get("rad_type") == "nelson_c":
                    rad_nelson_c = bla.text;
                if bla.get("rad_type") == "classical":
                    rad_classical = bla.text;
            
            print kanji, stroke_count, rad_classical, rad_nelson_c
            sql = "INSERT OR IGNORE INTO kanji_kanji (kanji, stroke_count, rad_value_classical, rad_value_nelson) VALUES (?,?,?,?);"
            self.c.execute(sql, [kanji, stroke_count, rad_classical, rad_nelson_c])
            rowid = self.c.lastrowid
            
            # Get the reading_meaning groups
            reading_meaning = entry.find("reading_meaning")
            if reading_meaning is None:
                continue    
            # rmgroup

            rmgroups = [rmgroup for rmgroup in reading_meaning.findall("rmgroup")]
            for i in range(len(rmgroups)):
                print rowid, i
                sql = "INSERT OR IGNORE INTO kanji_rmgroup (kanji_id, group_id) VALUES (?,?);"
                self.c.execute(sql, [rowid, i])
                
                readings = rmgroup.findall("reading")
                for reading in readings:
                    print rowid, i, reading.text, reading.get("r_type")
                    sql = "INSERT OR IGNORE INTO kanji_reading (kanji_id, group_id, reading, r_type) VALUES (?,?,?,?);"
                    self.c.execute(sql, [rowid, i, reading.text, reading.get("r_type")])
            
                meanings = rmgroup.findall("meaning")
                for meaning in meanings:
                    if meaning.get("m_lang", "en") == "en":
                        print rowid, i, meaning.text
                        sql = "INSERT OR IGNORE INTO kanji_meaning (kanji_id, group_id, meaning) VALUES (?,?,?);"
                        self.c.execute(sql, [rowid, i, meaning.text])
                                
            # nanori
            nanoris = [nanori for nanori in reading_meaning.findall("nanori")]
            for nanori in nanoris:
                print rowid, nanori.text
                sql = "INSERT OR IGNORE INTO kanji_nanori (kanji_id, nanori) VALUES (?,?);"
                self.c.execute(sql, [rowid, nanori.text])

tables_sql = [
        # Vocabulary
        '''CREATE TABLE IF NOT EXISTS vocab_karo  
            (id INTEGER PRIMARY KEY,
            k_ele TEXT,
            r_ele TEXT,
            UNIQUE(r_ele, k_ele));''',
        '''CREATE TABLE IF NOT EXISTS vocab_meaning  
            (id INTEGER PRIMARY KEY,
            karo_id INTEGER,
            meaning TEXT,
            UNIQUE(karo_id, meaning));''',
        '''CREATE TABLE IF NOT EXISTS vocab_partofspeech
            (id INTEGER PRIMARY KEY,
            karo_id INTEGER,
            pos TEXT,
            UNIQUE(karo_id, pos));''',
        # Kanji
        '''CREATE TABLE IF NOT EXISTS kanji_kanji
            (id INTEGER PRIMARY KEY,
            kanji TEXT,
            stroke_count INTEGER,
            rad_value_classical INTEGER,
            rad_value_nelson INTEGER,
            UNIQUE(kanji));''',
        '''CREATE TABLE IF NOT EXISTS kanji_rmgroup
            (kanji_id INTEGER,
            group_id INTEGER,
            UNIQUE(kanji_id, group_id));''',
        '''CREATE TABLE IF NOT EXISTS kanji_reading
            (id INTEGER PRIMARY KEY,
            kanji_id INTEGER,
            group_id INTEGER,
            reading TEXT,
            r_type TEXT,
            UNIQUE(kanji_id, group_id, reading, r_type));''',
        '''CREATE TABLE IF NOT EXISTS kanji_meaning
            (id INTEGER PRIMARY KEY,
            kanji_id INTEGER,
            group_id INTEGER,
            meaning TEXT,
            UNIQUE(kanji_id, group_id, meaning));''',
        '''CREATE TABLE IF NOT EXISTS kanji_nanori
            (id INTEGER PRIMARY KEY,
            kanji_id INTEGER,
            nanori TEXT,
            UNIQUE(kanji_id, nanori));''',
        # Compounds
        '''CREATE TABLE IF NOT EXISTS compounds
            (id INTEGER PRIMARY KEY,
            kanji_id INTEGER,
            vocab_meaning_id INTEGER,
            UNIQUE(kanji_id, vocab_id));''',
        # Scores
        '''CREATE TABLE IF NOT EXISTS scores
            (user TEXT,
            type TEXT,
            entry_id INTEGER,
            UNIQUE(user, type, entry_id));''',
        # Lists
        '''CREATE TABLE IF NOT EXISTS lists
            (list TEXT,
            level INTEGER,
            type TEXT,
            entry_id INTEGER,
            UNIQUE(list, level, type, entry_id));''']   
          

'''
f = codecs.open("JMdict.xml", 'r', encoding = "utf-8")
o = codecs.open("JMdict_pos.xml", 'w', encoding = "utf-8")

for line in f:
    part1 = line.replace("<pos>&", "<pos>")
    part2 = part1.replace(";</pos>", "</pos>")
    o.write(part2)

f.close()
o.close()
'''

def parse_jmdict(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for query in tables_sql:
        c.execute(query)
    
    conn.commit()
    
    jmdict = JMDict("JMdict_pos.xml", c)
    
    #do mah thang
    jmdict.insert_into_db()
        
    conn.commit()
    c.close()
    
def parse_kanjidic2(db):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    for query in tables_sql:
        c.execute(query)
    
    conn.commit()
    
    kanjidic = KanjiDic2("kanjidic2.xml", c)
    
    #do mah thang
    kanjidic.insert_into_db()
        
    conn.commit()
    c.close()
    
parse_jmdict("japanesetest.db")
parse_kanjidic2("japanesetest.db")
