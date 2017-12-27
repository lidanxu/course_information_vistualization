#-*- coding:utf-8 -*-
from __future__ import division 
import pymongo
from pymongo import MongoClient
import math
import re 
import jieba
import jieba.analyse 
import json 
import sys 
from collections import OrderedDict
#f_out = open('./weibo_topic','w')
#sys.stdout = f_out 

def read_data():
    client = MongoClient('xx.xx.xx.xx',27017)
    db = client.weibo_lg
    
    weibo_comments = db.weibo_comments 
    weibo_messages = db.weibo_messages 

    comments = [];messages = []
    #time_topic = {}
    #user_end1 = [];user_end2 = []
    for c in weibo_comments.find():
        #key = c['Time_Pub'].day
        #time_topic.setdefault(key,[])
        comments.append(c['Text'])
        #time_topic[key].append(c['Text'])
        '''
        try:
            user_end1.append(c['Tools'])
        except:
            pass 
        '''
    for m in weibo_messages.find():
        #key = m['Time_Pub'].day 
        #time_topic.setdefault(key,[])
        #time_topic[key].append(m['Text'])
        messages.append(m['Text'])

        #messages.append(m['Text']) 
        '''
        try:
            user_end2.append(m['Tools'])
        except:
            pass
        '''

    return comments,messages 

#read from mongodb
def read_data1():
    client = MongoClient('xx.xx.xx.xx',27017)
    db = client.weibo_lg
    
    weibo_comments = db.weibo_comments 
    weibo_messages = db.weibo_messages 

    #comments = [];messages = []
    time_topic = {}
    #user_end1 = [];user_end2 = []
    for c in weibo_comments.find():
        key = c['Time_Pub'].day
        time_topic.setdefault(key,[])
        time_topic[key].append(c['Text'])
        '''
        try:
            user_end1.append(c['Tools'])
        except:
            pass 
        '''
    for m in weibo_messages.find():
        key = m['Time_Pub'].day 
        time_topic.setdefault(key,[])
        time_topic[key].append(m['Text'])

        #messages.append(m['Text']) 
        '''
        try:
            user_end2.append(m['Tools'])
        except:
            pass
        '''

    return time_topic 

def fenci(text):
    f_stop = open('stopwords','r')
    addlist = ['\n',',',"\n"]
    stoplist = []
    for l in f_stop:
        stoplist.append(re.split('\n',l.decode('utf8'))[0])
    f_stop.close()
    
    sentence = ','.join(text)
    text = re.sub(r'[a-zA-Z0-9.。：:;；，,)）(（！!?？”“\"]','',sentence).split()
    text1 = []
    for t in text:
        t2 = []
        texts = jieba.cut(t)
        for t1 in texts:
            if t1 not in stoplist and t not in addlist and len(t)>1:
                t2.append(t1)
        text1.append(t2)
    return text1 

def key_word(comments,messages):
    
    comments.extend(messages)
    text1 = fenci(comments)
    return text1 

def make_idf_file(text):
    id_freq = {}
    le = len(text)
    for doc in text:
        doc = set(x for x in doc)
        for x in doc:
            id_freq.setdefault(x,0)
            id_freq[x] += 1
    with open('idf_text','w') as f:
        for key,value in id_freq.items():
            str1 = key +' '+str(math.log(le/(value+1),2))+'\n'
            f.write(str1.encode('utf8'))

def tfidf_text(sentence): 
    jieba.analyse.set_idf_path('idf_text')
    tags = jieba.analyse.extract_tags(sentence,topK=250,withWeight=True)
    with open('tfidf_word','w') as f:
        for x,w in tags:
            w1 = int(math.sqrt(w)/(1+math.exp(-w))*10000)
            str1 = '"'+x+'"'+':'+str(w1) +",\n"
            f.write(str1.encode('utf8'))
 
def topic_static(data_dict):
    dict1 = {}
    for key,values in data_dict.items():
        dict1.setdefault(key,{})
        for v in values:
            m = re.findall(r'#(.*?)#',v)
            for i in  m:
                if 20>len(i)>1:
                    i = i.encode('utf8')
                    dict1[key].setdefault(i,0)
                    dict1[key][i] += 1

    #for day,topics in dict1.items():
    return dict1 

def dict_to_json(dict1):
    json_data = json.dumps(dict1)
    with open('./topic_weibo.json','w') as outfile:
        json.dump(json_data,outfile)



if __name__ =='__main__':
    data_dict = read_data1()
    dict1 = topic_static(data_dict)
    #dict4 = {}
    for key,values in dict1.items():
        dict2 = sorted(values.items(),key=lambda values:values[1],reverse=True)
        list1 = dict2[:30]
        dict3 = OrderedDict(list1)
        print key 
        for k,v in dict3.items():
            print k,v
    #dict_to_json(dict3)
    #comments,messages,user_end1,user_end2 = read_data()
    #text1 = key_word(comments,messages)
    #make_idf_file(text1)
    #text2 = []
    #for t in text1:
    #    text2.append(','.join(t))
    #sentence = ','.join(text2)
    #tfidf_text(sentence)



