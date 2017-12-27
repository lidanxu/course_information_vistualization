#-*- coding:utf-8 -*-

#使用lda模型挖掘文本主题

from weibo_ import *
from gensim import corpora,models,similarities
from gensim.models import  LdaModel
import json
import sys
f_out = open('lda_topic','w')
sys.stdout  = f_out 

def test(key,text1): 
    #comments,messages = read_data()
    #text1 = key_word(comments,messages)
    #生成字典
    dictionary = corpora.Dictionary(text1)
    #生成语料库i
    corpus = [dictionary.doc2bow(text) for text in text1]
    #tfidf加权
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    p_list = []
    topicnum_list = []
    num_topic = 2
    #for i in range(2,50):
    #    num_topics = i
    lda = LdaModel(corpus= corpus_tfidf,id2word=dictionary,num_topics=num_topic)
    #perplex = lda.log_perplexity(corpus_tfidf)
    #p_list.append(perplex)
    #topicnum_list.append(num_topics)
    topics = lda.print_topics()
    print '*'*50
    print key,':'
    for i in topics:
        str1 = str(i[0])+':'
        print str1,i[1].encode('utf8')
    



    #return topicnum_list,p_list 

def list_to_json(keys,values):
    dict1 = dict(zip(keys,values))
    json_data = json.dumps(dict1)
    with open('./top_perplex','w') as outfile:
        json.dump(json_data,outfile)


if __name__ == '__main__':
    #topicnum_list,p_list = test()
    #list_to_json(topicnum_list,p_list)
    time_topic = read_data()
    #text1 = []
    for key ,text in time_topic.items():
        #text1 = [ i for i in text ]
        text2 = fenci(text)
        test(key,text2)




