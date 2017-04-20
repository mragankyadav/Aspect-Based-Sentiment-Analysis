from stemming.porter2 import stem
from data_parser import outputParser
worddict={}
def processopinions():
    fr=open('dataset/subjclueslen1-HLTEMNLP05.tff')
    for line in fr:
        words=line.split()
        if len(words)>0:
            worddict[words[2].split("=")[1]]=words[5].split("=")[1]

def findpol():
    processopinions()
    fw=open("generated_files/withPolarities.txt",'w')
    testdata=outputParser.write_out("generated_files/crf_output.txt")
    # print testdata
    # print len(testdata),
    # print "here"
    dataforacc={}
    for k,v in testdata.iteritems():
        fw.write("Text: "+k+"\n")
        dataforacc[k]={}
        copy=k
        k=k.replace('.',' ').replace('!',' ').replace('-',' ')

        sent=[stem(word) for word in k.split()]
        if len(v)!=0:
            fw.write("Aspect Terms\n")
            for i in v:
                p=n=0
                idx=k.split().index(i)
                # print sent[idx]
                for j in range(max(0,idx-10),min(len(sent),idx+10)):
                    try:
                        if worddict[sent[j]]=="positive":
                            p+=1
                        elif worddict[sent[j]]=="negative" :
                            n+=1
                    except KeyError:
                        pass
                if p>n:
                    fw.write("Aspect="+i+" "+"Polarity="+"positive\n")
                    dataforacc[copy][i]="positive"
                elif p<n:
                    fw.write("Aspect=" + i + " " + "Polarity=" + "negative\n")
                    dataforacc[copy][i] = "negative"
                else:
                    fw.write("Aspect=" + i + " " + "Polarity=" + "neutral\n")
                    dataforacc[copy][i] = "positive"
        else:
            fw.write("Aspect Terms: None\n")
        fw.write("\n")
    fw.close()
    return dataforacc


