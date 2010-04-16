# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET

class JMDict():
    def __init__(self,path):
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()

    def getNextTuple(self):

        for entry in self.root: #(entry for entry in self.root if (entry.find("ent_seq").text == "1000000")):
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
                reblist = (r_ele.find("reb").text for r_ele in entry.findall("r_ele") if r_ele.find("re_restr") == None or r_ele.find("re_restr").text == keb)
                        
                for reb in reblist:
                    # Every single gloss (in a "sense" entry) belongs to all the rebs/kebs, so no conditionals here.
                    # However, we don't want any foreign meanings, so the language has to be english (default).
                    for sense in entry.findall("sense"):
                        for meaning in (gloss.text for gloss in sense.findall("gloss") if gloss.get("{http://www.w3.org/XML/1998/namespace}lang", "eng") == "eng"):
                            yield (keb,reb,meaning)
                            
jmdict = JMDict("JMdict.xml")
thinggen = jmdict.getNextTuple()
for i in range(100):
    print thinggen.next()