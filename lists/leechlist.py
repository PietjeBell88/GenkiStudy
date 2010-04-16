import urllib
import re
from tableparser import *
from lxml import html
import codecs
from HTMLParser import HTMLParser

f = codecs.open("testbestand.txt", 'w')
f.write(
'''! language = Japanese
! listname = Genki Elementary
! levelorder = Ascending


! ltype = vocab
! lformat = r_ele, k_ele, meaning
''')


for i in range(1,24):
    url = urllib.urlopen('http://aitweb.csus.edu/fl/japn/genki_vocab_table.php?lesson=%d' % i)
    p = TableParser()
    p.feed(url.read())
    url.close()
    table = p.doc[0]
    f.write("\n! level = %d\n" % i)
    for item in table[1:]:
        if i < 3:
            item2 = item[0:2]
            item2.append(item[3])
            item = item2
        f.write("\t".join(item) + "\n")
        
f.write('''

! ltype = kanji
! lformat = kanji, reading, meaning
''')
for i in range(3,24):
    url = urllib.urlopen('http://aitweb.csus.edu/fl/japn/genki_kanji_table.php?lesson=%d' % i)
    p = TableParser()
    text = url.read()
    url.close()
    text = re.sub("<a href=javascript:.*?>(.*?)</a>","\\1",text)
    text = re.sub("\n","",text)
    p.feed(text)
    table = p.doc[0]
    f.write("\n! level = %d\n" % i)
    for item in table[1:]:
        f.write("\t".join(item[0:3]) + "\n")

f.write('''

! ltype = compounds
! lformat = compound, reading, meaning
''')
for i in range(1,322):
    url = urllib.urlopen('http://aitweb.csus.edu/fl/japn/genki_kanji_examples.php?id=%d' % i)
    p = TableParser()
    text = url.read()
    if "No examples available yet" in text:
        continue
    p.feed(text)
    url.close()
    table =  p.doc[0]
    #f.write("\n! level = %d\n" % i)
    for item in table[1:]:
        f.write("\t".join(item) + "\n")


f.close()


