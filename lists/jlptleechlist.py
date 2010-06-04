# -*- coding: utf-8 -*-
import urllib
import re
import sys
from tableparser import *
from lxml import html
import codecs
from HTMLParser import HTMLParser

def kanjilist(f, i):
    f.write('''

! ltype = kanji
! lformat = kanji, reading, meaning
''')

    url = urllib.urlopen('http://www.jlptstudy.com/N%d/N%d_kanji-list_detail.html' % (i,i))
    text = url.read()
    url.close()
    
    matches = re.findall('<div class="(.*?)">(.*?)</div>',text)
    
    kanji = None;
    k_meanings = None;
    k_readings = [];
    
    a_kanji = []
    for type, value in matches:
        #print type, value
        if type.startswith("kanjiChar"):
            kanji = value;
        if type.startswith("kMeaning"):
            k_meanings = [meaning.strip() for meaning in value.split(",")]
        if type.startswith("readings"):
            k_readings += [reading.strip() for reading in value.split(",")]
        if type.startswith("compHeading"):
            #write kanji
            #print kanji + "\t" + "; ".join(k_readings) + "\t" + "; ".join(k_meanings)
            a_kanji += (kanji, "; ".join(k_readings), "; ".join(k_meanings))
            f.write("\t".join([kanji, "; ".join(k_readings), "; ".join(k_meanings)]) + "\n")
            k_readings = [];
    
    f.write('''

! ltype = compounds
! lformat = k_ele, r_ele, meaning
''')
    a_compounds = []
    k_ele = None
    for type, value in matches:
        #print type, value
        if type.startswith("compChar"):
            k_ele = value
        if type.startswith("compKana"):
            r_ele = value
        if type.startswith("compTrans"):
            c_meaning = value.replace(",", ";")
        if type.startswith("kanjiChar") and k_ele:
            #print k_ele + "\t" + r_ele  + "\t" + c_meaning
            a_compounds += (k_ele, r_ele, c_meaning)
            f.write("\t".join([k_ele, r_ele, c_meaning]) + "\n")
    #p = TableParser()
    #p.feed(text)
    #table = p.doc[0]
    #print text
    #print table[0][1]

def vocablist(f, i):
    f.write(
'''

! ltype = vocab
! lformat = k_ele, r_ele, meaning
''')
    url = urllib.urlopen('http://jlptstudy.com/N%d/N%d_vocab-list.html' % (i,i))
    text = url.read()
    url.close()
    p = TableParser()
    p.feed(text)
    table = p.doc[0]
    #f.write("\n! level = %d\n" % i)
    for nr, r_ele, k_ele, pos, meanings in table[1:]:
        #print "\t".join([k_ele, r_ele, meanings.replace(",", ";")])
        f.write("\t".join([k_ele, r_ele, meanings.replace(",", ";")]) + "\n")
f = codecs.open("jlptest.txt", 'w')
f.write(
'''! language = Japanese
! listname = JLPT New
! levelorder = Descending

''')

for i in [5,4]:
    f.write("\n! level = %d\n" % i)
    vocablist(f, i)
    kanjilist(f, i)

f.close()