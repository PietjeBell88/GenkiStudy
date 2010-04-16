import operator
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re
import itertools
import codecs
import sqlite3
import sys
import os
 
       
class MyWindow(QWidget):
    def __init__(self, *args):
        QWidget.__init__(self, *args)
        self.setWindowTitle("Sorting PyQT's QTableView")
        self.setGeometry(300, 200, 600, 500)
        
        self.listview = self.createList()
        self.tableview = self.createTable(self.listmodel.data[0])
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.listview.setSizePolicy(sizePolicy)
        layout = QHBoxLayout()
        layout.addWidget(self.listview)
        layout.addWidget(self.tableview)
        self.setLayout(layout)
        self.connect(self.listview, SIGNAL("activated(QModelIndex)"), self.updateTable)
    
    def updateTable(self, index):
        print index.row()
        print self.listmodel.data[index.row()]
        self.tmodel.changeTable(self.listmodel.data[index.row()])
        self.tview.resizeColumnsToContents()

    def createTable(self, tablename):
        self.tview = QTableView()
        self.tmodel = MyTableModel(self, tablename)
        self.tview.setModel(self.tmodel)
        self.tview.setShowGrid(False)
        vh = self.tview.verticalHeader()
        vh.setVisible(False)
        hh = self.tview.horizontalHeader()
        self.tview.resizeColumnsToContents()
        nrows = self.tmodel.rowCount()
        for row in range(nrows):
            self.tview.setRowHeight(row, 18)
        self.tview.setSortingEnabled(True)
        return self.tview
    
    def createList(self):
        listview = QListView()
        self.listmodel = MyListModel(self)
        listview.setModel(self.listmodel)
        listview.setResizeMode(QListView.Fixed)
        return listview
    
    
class MyListModel(QAbstractListModel):
    def __init__(self, parent, *args):
        QAbstractListModel.__init__(self, parent, *args)
        
        self.conn = sqlite3.connect('test.db')
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
 

class MyTableModel(QAbstractTableModel):
    def __init__(self, parent, tablename, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        
        self.conn = sqlite3.connect('test.db')
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
    
 
 
app = QApplication(sys.argv)
win = MyWindow()
win.show()
sys.exit(app.exec_())