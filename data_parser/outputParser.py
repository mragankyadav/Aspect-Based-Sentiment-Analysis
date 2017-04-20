def write_out( filename):
    testdata={}
    crf = open(filename, 'r')
    with open("generated_files/restaurants_predicted.txt", 'w') as o:
        aspects = []
        sent = []
        for line in crf:
            words=line.split()
            if len(words)>0:
                if words[0]!=".":
                    sent.append(words[0])
                    if words[3]=="True":
                        aspects.append(words[0])
                else:
                    o.write("Text: "+' '.join(sent)+"\n")
                    if len(aspects)==0:
                        o.write("Aspect Terms:None\n")
                    else:
                        o.write("Aspect Terms:\n")
                        for i in aspects:
                            o.write(i+"\n")
                    testdata[' '.join(sent)+"."]=aspects
                    sent=[]
                    aspects=[]
                    o.write("\n")
    return testdata

