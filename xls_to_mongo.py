#-*- coding:utf-8 -*-

import xlrd
import pymongo
from pymongo import MongoClient

def read_xls(path,sheet=0):
    data = xlrd.open_workbook(path)
    sh = data.sheet_by_index(sheet)

    columns = sh.row(0)
    columns_list = []
    for i in columns:
        columns_list.append(i.value)
    
    documents = []
    for i in range(1,sh.nrows):
        row = sh.row(i)
        document ={}
        for r in range(len(row)):
            document.setdefault(columns_list[r],row[r].value)
        documents.append(document)
    return documents 

def save_to_mongo(documents):
    client =MongoClient('xx.xx.xx.xx',27017)
    db = client.weibo_lg
    co = db.weibo 

    #insert 
    co.sert_many(documents)


