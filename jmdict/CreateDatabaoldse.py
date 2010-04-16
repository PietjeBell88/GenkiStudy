# -*- coding: utf-8 -*-
import re
import itertools
import codecs
import sqlite3
import sys
import os

class List:
    def __init__(self, file):
        self.config = {"language": "",
                       "listname": "",
                       "levelorder": "",
                       "ltype": "",
                       "level": "",
                       "lformat": ""}
        self.lines = []
        self.file = file

    def parseFile(self):
        for line in self.file:
            # Strip the BOM from the beginning of the Unicode string, if it exists
            line = line.lstrip( unicode( codecs.BOM_UTF8, "utf8" ) )
            # Strip leaind and trailing whitespace
            line = line.strip()
            if line.startswith("#") or line == "":
                # Ignore comments and empty lines
                continue
            elif line.startswith("!"):
                self.parseConfigLine(line)
                continue
            elif "" not in self.config.values():
                self.lines.append(Line(self.config, line))
            else:
                print "...." + line
                print "wanted to add something, but not all config values were set"
                sys.exit(1)

    def parseConfigLine(self, line):
        # Parses the config line
        key, value = map(unicode.strip, re.split('=',line.strip()[1:]))
        if key not in self.config:
            raise Exception, "Unknown config key: " + key
            sys.exit(1)
        else:
            self.config[key] = value

    def insertSql(self, c):
        for line in self.lines:
            line.insertSql(c)

class Line:
    def __init__(self, config, entry):
        self.config = config

        # These lines permutate the entries, because that is how
        # the should be written to the database.
        splitted = re.split('\\t',entry)
        splitted = [map(unicode.strip, re.split(';',x)) for x in splitted]
        self.entry = itertools.product(*splitted)
        
    def insertSql(self, c):
        columns = map(unicode.strip, re.split(',',self.config["lformat"]))
        for subentry in self.entry:
            req_where = " AND ".join([x + " = ?" for x in columns])
            
            sql = "SELECT rowid FROM " + self.config["ltype"] + " WHERE " + req_where + ";"
            print sql, subentry
            c.execute(sql, subentry)
            
            results = c.fetchall()
            print results
            n = len(results)
            # If somehow the amount of rows returned was -1, or there were multiple hits
            # which should be impossible, throw an error and continue.
            if (n == 1):
                print "Entry already exists\n", subentry
                rowid = results[0][0]
            elif (n == 0):
                print "Entry does not exist, inserting...\n", subentry
                
                sql = "INSERT INTO " + self.config["ltype"] + " (" + self.config["lformat"] + ") VALUES (" + ",".join("?" * len(subentry)) + ");"
                print sql, subentry
                c.execute(sql, subentry)
                
                rowid = c.lastrowid
            else:
                raise Exception, "Too many rows, or something went wrong"
                continue  
            
            sql = "INSERT OR IGNORE INTO " + "lists" + " VALUES (" + ",".join("?"*4) + ");"
            c.execute(sql, (self.config["ltype"], rowid, self.config["listname"], self.config["level"]))

        
conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS vocab
             (id INTEGER PRIMARY KEY,
              r_ele TEXT,
              k_ele TEXT,
              meaning TEXT);''')
c.execute('''CREATE TABLE IF NOT EXISTS lists
            (type TEXT,
             id INTEGER,
             list TEXT,
             level INTEGER);''')
conn.commit()

f = codecs.open("Genki_Elementary.list", 'r', encoding = "utf-8")
thelist = List(f)
thelist.parseFile()
thelist.insertSql(c)
conn.commit()
c.close()
