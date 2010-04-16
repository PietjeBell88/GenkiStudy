import operator
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import bisect
import re
import itertools
import codecs
import sqlite3
import sys
import os


class DatabaseListModel(QAbstractListModel):
    
    def __init__(self, parent, pathtodb, *args):
        QAbstractListModel.__init__(self, parent, *args)

        self.conn = sqlite3.connect(pathtodb)
        self.c = self.conn.cursor()
        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        results = self.c.fetchall()
        print results
        self.data = [x[0] for x in results]

    def __del__(self):
        self.conn.commit()
        self.c.close()


    def rowCount(self, parent=None):
        return len(self.data)


    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.data[index.row()])


class DatabaseTableModel(QAbstractTableModel):
    
    def __init__(self, parent, pathtodb, tablename, *args):
        QAbstractTableModel.__init__(self, parent, *args)

        self.conn = sqlite3.connect(pathtodb)
        self.c = self.conn.cursor()

        self.tablename = tablename

        self.setHeader()

        self.order = "ASC"
        self.data = None

        self.reloadData()


    def __del__(self):
        self.conn.commit()
        self.c.close()


    def rowCount(self, parent=None):
        return len(self.data)


    def columnCount(self, parent=None):
        return len(self.header)


    def changeTable(self, tablename):
        self.tablename = tablename
        self.setHeader()
        self.reset()


    def setHeader(self):
        self.c.execute("PRAGMA table_info(%s);" % self.tablename)
        results = self.c.fetchall()
        self.header = [x[1] for x in results]
        self.sort = self.header[0]


    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.data[index.row()][index.column()])


    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header[col])
        return QVariant()


    def sort(self, col, order):
        self.sort = self.header[col]
        if order == Qt.DescendingOrder:
            self.order = "DESC"
        else:
            self.order = "ASC"
        self.reset()


    def reloadData(self):
        sql = "SELECT * FROM %s ORDER BY %s %s;" % (self.tablename, self.sort, self.order)
        print sql
        self.c.execute(sql)
        self.data = self.c.fetchall()


    def reset(self):
        self.reloadData()
        QAbstractTableModel.reset(self)



KEY, NODE = range(2)


class BranchNode:

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.scoretarget = 20

    def orderKey(self):
        return self.name.lower()


    def toString(self):
        return self.name


    def __len__(self):
        return len(self.children)


    def childAtRow(self, row):
        assert 0 <= row < len(self.children)
        return self.children[row][NODE]
        

    def rowOfChild(self, child):
        for i, item in enumerate(self.children):
            if item[NODE] == child:
                return i
        return -1


    def childWithKey(self, key):
        if not self.children:
            return None
        i = bisect.bisect_left(self.children, (key, None))
        if i < 0 or i >= len(self.children):
            return None
        if self.children[i][KEY] == key:
            return self.children[i][NODE]
        return None

    def insertChild(self, child):
        child.parent = self
        bisect.insort(self.children, (child.orderKey(), child))

    def field(self, column):
        assert 0 <= column <= 1
        if column == 0:
            return self.name
        else:
            items, score = self.wScore()
            return str((100*score)/(items*self.scoretarget)) + "%"
                       
    def wScore(self):
        items = 0
        score = 0;
        for node in self.children:
            node = node[NODE]
            nitems, nscore = node.wScore()
            items += nitems
            score += nscore
            
        return (items, score)        
        
    def hasLeaves(self):
        if not self.children:
            return False
        return isinstance(self.children[0], LeafNode)


class LeafNode:

    def __init__(self, fields, score, parent=None):
        self.parent = parent
        self.fields = fields
        self.score = score
        self.scoretarget = 20


    def orderKey(self):
        return u"\t".join(self.fields).lower()


    def toString(self, separator="\t"):
        return separator.join(self.fields)


    def __len__(self):
        return len(self.fields) + 1


    def asRecord(self):
        record = []
        branch = self.parent
        while branch is not None:
            record.insert(0, branch.toString())
            branch = branch.parent
        assert record and not record[0]
        record = record[1:]
        return record + self.fields + [self.score]


    def field(self, column):
        assert 0 <= column <= 1
        if column == 0:
            return self.toString()
        else:
            return str(self.score)

    def wScore(self):
        if self.score <= self.scoretarget:
            return (1, self.score)
        else:
            return (1, self.scoretarget)
        
        
class DatabaseTreeModel(QAbstractItemModel):

    def __init__(self, pathtodb, parent=None):
        QAbstractItemModel.__init__(self, parent)
        
        self.conn = sqlite3.connect(pathtodb)
        self.c = self.conn.cursor()
        
        self.columns = 2
        self.nesting = 3
        self.root = BranchNode("")
        self.headers = ["blubblub", "gedoe"]
        self.loadData()


    def loadData(self):
        self.root = BranchNode("")
        exception = None
        sql = '''SELECT lists.type, lists.list, lists.level, %(table)s.r_ele, %(table)s.k_ele, %(table)s.meaning, score%(table)s.meaning_je FROM %(table)s INNER JOIN lists ON %(table)s.id=lists.id LEFT OUTER JOIN score%(table)s ON lists.id=score%(table)s.id WHERE lists.type=? AND score%(table)s.user=?;''' % {'table': 'vocab'}
        self.c.execute(sql,('vocab', 'Pietje'))
        for row in self.c:
            self.addRecord(row, callReset=False)


    def addRecord(self, fields, callReset=True):
        root = self.root
        branch = None
        for i in range(self.nesting):
            fieldsi = fields[i] if not isinstance(fields[i],int) else "Level " + str(fields[i])
            key = fieldsi.lower()
            branch = root.childWithKey(key)
            if branch is not None:
                root = branch
            else:
                branch = BranchNode(fieldsi)
                root.insertChild(branch)
                root = branch
        assert branch is not None
        branch.insertChild(LeafNode(fields[self.nesting:-1], fields[-1], branch))
        if callReset:
            self.reset()
            
    def asRecord(self, index):
        leaf = self.nodeFromIndex(index)
        if leaf is not None and isinstance(leaf, LeafNode):
            return leaf.asRecord()
        return []
    
                
    def rowCount(self, parent):
        node = self.nodeFromIndex(parent)
        if node is None or isinstance(node, LeafNode):
            return 0
        return len(node)


    def columnCount(self, parent):
        return self.columns


    def data(self, index, role):
        if role == Qt.TextAlignmentRole:
            return QVariant(int(Qt.AlignTop|Qt.AlignLeft))
        if role != Qt.DisplayRole:
            return QVariant()
        node = self.nodeFromIndex(index)
        assert node is not None
        return QVariant(node.field(index.column()))


    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and \
           role == Qt.DisplayRole:
            assert 0 <= section <= len(self.headers)
            return QVariant(self.headers[section])
        return QVariant()



    def index(self, row, column, parent):
        assert self.root
        branch = self.nodeFromIndex(parent)
        assert branch is not None
        return self.createIndex(row, column,
                                branch.childAtRow(row))

    def parent(self, child):
        node = self.nodeFromIndex(child)
        if node is None:
            return QModelIndex()
        parent = node.parent
        if parent is None:
            return QModelIndex()
        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()
        row = grandparent.rowOfChild(parent)
        assert row != -1
        return self.createIndex(row, 0, parent)


    def nodeFromIndex(self, index):
        return index.internalPointer() \
            if index.isValid() else self.root
            


