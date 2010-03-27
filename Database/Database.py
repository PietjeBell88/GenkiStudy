# -*- coding: utf-8 -*-

import re
import itertools
import codecs
import sqlite3
import sys
import os

class DatabaseEntry:
    def __init__(self):
        raise AbstractClassError
    
    def getSQL(self):
        raise NotImplementedError
    

class Database():
    def __init__(self,language):
        if isinstance(language,Language) == False:
            print 'The argument "language" is not an instance of Language.'
            raise TypeError
        
        self.conn = sqlite3.connect(language.getPath())
        self.c = conn.cursor()
        for command in language.makeTables():
            c.execute(command)
        
    def Insert(self,object):
        isinstance(object,VocabEntry)
        isinstance(object,KanjiEntry)
        isinstance(object,ListEntry)
        isinstance(object,ScoreEntry)
        

def readLists():
    for filename in os.listdir("."):
        if (filename.endswith('.list')):
            print "1"
        print "2"
    return
    



    

