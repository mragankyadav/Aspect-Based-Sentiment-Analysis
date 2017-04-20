from __future__ import division
import os

import xml.etree.ElementTree as ET


def generateCleanTestData(test_filename):
    testdata={}
    tree = ET.ElementTree(file=test_filename)
    sentences = tree.getroot()
    count=0
    fileexist = os.path.exists('generated_files/cleanTestData.txt')
    if fileexist:
        f = open('generated_files/cleanTestData.txt', 'r')
    else:
        f = open('generated_files/cleanTestData.txt', 'w')

    for sentence in sentences:
        terms = []
        for elem in sentence.iter():
            if elem.tag=='text':
                line= elem.text
                testdata[line] = terms
                if not fileexist:
                    f.write(line+"\n")
            if elem.tag=='aspectTerm':
                aspect= elem.attrib['term']
                testdata[line].append(aspect)
    f.close()
    generatePOS_NE_tags("generated_files/cleanTestdata.txt",testdata)

def generatePOS_NE_tags(cleanDataPath,testdata):
    if not os.path.exists("generated_files/taggedtestFile.txt"):
        script = "./tagchunk.i686 -predict . w-5 "+cleanDataPath+" resources > generated_files/taggedtestFile.txt"
        os.system(script)
    generateConll(testdata)

def generateConll(testdata):
    fw=open('generated_files/test.data','w')
    fr=open('generated_files/taggedtestFile.txt','r')
    for line in fr:
        for word in line.split():
            first = word.split("_")[0]
            if first[len(first) - 1] == '.':
                first = first[:len(first) - 1]
            fw.write(first+"\t"+word.split("_")[1]+"\t"+word.split("_")[2]+"\n")
        fw.write("." + "\t" + "." + "\t" + "." + "\n")


    fw.close()

def traindatapath(path):
    test_filename =path
    generateCleanTestData(test_filename)