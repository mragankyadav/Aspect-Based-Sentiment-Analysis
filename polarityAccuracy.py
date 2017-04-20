from __future__ import division
from data_parser import outputParser

import xml.etree.ElementTree as ET
import polarity


def evaluate(train_filename):
    orgnlData={}
    testdata={}
    tree = ET.ElementTree(file=train_filename)
    sentences = tree.getroot()
    count=0
    for sentence in sentences:
        terms = []
        for elem in sentence.iter():
            aspect=[]
            if elem.tag=='text':
                line= elem.text
                orgnlData[line]=terms
            if elem.tag=='aspectTerm':
                aspect.append(elem.attrib['term'])
                aspect.append(elem.attrib['polarity'])
                orgnlData[line].append(aspect)


    testdata=polarity.findpol()
    precision=0
    recall=0
    orgtotal=0
    testtotal=0

    for k,v in testdata.iteritems():
        if k in orgnlData:
            # print v
            orgnalaspects=orgnlData[k]
            orgtotal+=len(orgnalaspects)
            testtotal+=len(v)
            for i in orgnalaspects:
                for key,val in v.iteritems():
                    if i[0]==key and i[1]==val:
                        precision+=1


    fr=open("generated_files/crf_output.txt",'r')
    for line in fr:
        words=line.split()
        if len(words)>0:
            if words[3]=="True":
                recall+=1
    # print orgnlData
    # print (testdata)
    # print (orgnlData)
    print "Precision=",
    precision=precision/testtotal
    print (precision)*100
    # recall=recall/orgtotal
    # print "Recall=",
    # print (recall)*100
    # a=precision*recall
    # b= precision+recall
    # f1=2*(a/b)
    # print "F-Score= "+str(f1*100)








