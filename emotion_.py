#-*- coding:utf-8 -*-

#2017.12.26
#使用情感词典判断语句的情感
from collections import defaultdict
from weibo_ import *
import jieba
import codecs
import re 
import chardet

def sentence_emotion(sentence,senDict,degreeDict):
    '''
    判断输入的sentence的情感
    返回sentence中的情感词，对应分数
    '''
    segList = jieba.cut(sentence)
    segList1 = [i for i in segList]
    #wordDict = defaultdict()
    valuelist = [i for i in range(len(segList1))]
    wordDict = dict(zip(segList1,valuelist))
    #print wordDict
    senWord,notWord,degreeWord,wordlist = classifyWords(wordDict,senDict,degreeDict)
    score = scoreSent(senWord,notWord,degreeWord,wordDict)
    return score,wordlist 

def classifyWords(wordDict,senDict,degreeDict):
    '''
    #情感词
    with open('BosonNLP_sentiment_score.txt','r') as f_in:
        senList = f_in.readlines()
    senDict = defaultdict()
   # nn = 0
    for s in senList:
       # nn += 1
        senDict[s.strip().split(' ')[0]] = s.strip().split(' ')[1]
    #程度副词
    degreeDict = degree()
    '''
    #否定词
    notList = [u"不",u"没",u"无",u"非",u"莫",u"弗",u"勿",u"毋",u"未",u"否",u"别",u"無",u"休",u"难道"]

    #定位
    senWord = defaultdict()
    notWord = defaultdict()
    degreeWord = defaultdict()
    wordlist = []

    for word in wordDict.keys():
        #print 'word :',word 
        #print chardet.detect(word) 
        if word in senDict.keys() and word not in notList and word  not in degreeDict:
            senWord[wordDict[word]] = senDict[word]
            wordlist.append(word)
        elif word in notList and word not in degreeDict.keys():
            notWord[wordDict[word]] = -1
        elif word in degreeDict.keys():
            degreeWord[wordDict[word]] = degreeDict[word]
    
    return senWord,notWord,degreeWord,wordlist 

def emotionWord():
    #情感词
    with open('BosonNLP_sentiment_score.txt','r') as f_in:
        senList = f_in.readlines()
    senDict = defaultdict()
   # nn = 0
    for s in senList:
       # nn += 1
        k = s.strip().split(' ')[0].decode('utf8')
        senDict[k] = float(s.strip().split(' ')[1])
    return senDict 

def degree():
    with open('degree.txt','r') as f_in:
        degree1 = f_in.readlines()
    num = 0
    dict1 = defaultdict() 
    nn = 0
    for d in degree1:
        nn += 1
        d = d.decode('GB2312')
        if '|' in d:
            num += 1
        dict1.setdefault(num,[])
        if '|' not in d:
            dict1[num].append(d.strip())
    degree_dict  = defaultdict()
    for key,values in dict1.items():
        if key == 1:
            weight = 2
        elif key == 2:
            weight =1.5
        elif key ==3:
            weight = 1.2
        elif key == 4:
            weight = 0.8
        elif key == 5:
            weight = 0.2
        else :
            weight = -0.5
        for i in values:
            degree_dict[i] =  weight 
    return degree_dict
    

def scoreSent(senWord,notWord,degreeWord,segResult):
    W  = 1
    score = 0
    #存所有情感词的位置的列表
    senLoc = senWord.keys()
    notLoc = notWord.keys()
    degreeLoc = degreeWord.keys()
    
    senloc = -1
    
    #遍历句中所有词，i为词绝对位置
    for i in range(0,len(segResult)):
        if i in senLoc:
            #loc 为情感词位置列表的序号
            senloc += 1
            #直接添加该情感词分数
            score += W*float(senWord[i])
            if senloc <len(senLoc)-1:
                #判断该情感词与下一情感词之间是否有否定词或者程度副词
                #j为绝对位置
                for j in range(senLoc[senloc],senLoc[senloc+1]):
                    #如果有否定词
                    if j in notLoc:
                        W *= -1
                    #如果有程度副词
                    elif j in degreeLoc:
                        W *= float(degreeWord[j])

        #i 定位至下一个情感词
        if senloc < len(senLoc)-1:
            i = senLoc[senloc + 1]
    return score 

def run():
    comments,messages = read_data()
    #text1 = key_word(comments,messages)
    comments.extend(messages)

    #comments = comments[:100]

    senDict = emotionWord()
    degreeDict = degree()
    dict_emo = {}
    weightlist = []
    wordlist1 = []
    num = 0
    for i in comments:
        num += 1
        #i = i
        weight,wordlist = sentence_emotion(i,senDict,degreeDict)
        if num%100 == 0:
            print '%d : weight:%s'%(num,weight)
        weightlist.append(weight)
        wordlist1.extend(wordlist)
    return weightlist,wordlist1

if __name__ =='__main__':
    weightlist,wordlist = run()
    with open('emotion_weight.txt','w') as f_out:
        for i in weightlist:
            f_out.write(str(i))
            f_out.write('\n')
    with open('emotion_word.txt','w') as f_out:
        print wordlist 
        for i in wordlist:
            try:
                f_out.write(i)
            except:
                f_out.write(i.encode('utf8'))
            f_out.write('\n')
