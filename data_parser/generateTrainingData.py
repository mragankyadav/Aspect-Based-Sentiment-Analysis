from __future__ import division
import xml.etree.ElementTree as ET
import os.path



def generateCleanData(train_filename):
    traindata={}
    tree = ET.ElementTree(file=train_filename)
    sentences = tree.getroot()
    count=0
    fileexist=os.path.exists('generated_files/cleanData.txt')
    # print os.listdir("generated_files")
    if fileexist:
        f = open('generated_files/cleanData.txt', 'r')
    else:
        f = open('generated_files/cleanData.txt', 'w')
    for sentence in sentences:
        terms = []
        for elem in sentence.iter():

            if elem.tag=='text':
                line= elem.text
                traindata[line] = terms
                if not fileexist:
                    f.write(line+"\n")
            if elem.tag=='aspectTerm':
                aspect= elem.attrib['term']
                traindata[line].append(aspect)
    f.close()
    generatePOS_NE_tags("generated_files/cleanData.txt",traindata)

def generatePOS_NE_tags(cleanDataPath,traindata):
    if not os.path.exists("generated_files/taggedtrainData.txt"):
        script = "./tagchunk.i686 -predict . w-5 "+cleanDataPath+" resources > generated_files/taggedtrainData.txt"
        os.system(script)
    generateConll(traindata)



def generateConll(traindata):
    if not os.path.exists("../generated_files/taggedtrainData.txt"):
        fw=open('generated_files/train.data','w')
        fr=open('generated_files/taggedtrainData.txt','r')

        for line in fr:
            cleanline=[]
            for i in line.split():
                cleanline.append(i.split("_")[0])
            cleanline=' '.join(cleanline)
            aspectTerms=[]
            for k,v in traindata.iteritems():

                if k==cleanline:
                    aspectTerms=v
                    # print aspectTerms
            for word in line.split():
                first = word.split("_")[0]
                if first[len(first) - 1] == '.':
                    first = first[:len(first) - 1]
                fw.write(first+"\t"+word.split("_")[1]+"\t"+word.split("_")[2])
                if word.split("_")[0] in aspectTerms:
                    fw.write("\t"+"True"+"\n")
                else:
                    fw.write("\t" + "False" + "\n")
            fw.write("." + "\t" + "." + "\t" + "." + "\t" +"False" "\n")

        fw.close()

def traindatapath(path):
    train_filename =path
    generateCleanData(train_filename)