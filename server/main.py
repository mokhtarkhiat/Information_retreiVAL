# back end 
import re 
import nltk
import string
import math

from nltk.probability import FreqDist 


#extract information from the file 
def extract_information():

    # read the file CACM 

    with open ("data/cacm.all") as cacm:
        listLines = cacm.readlines()
        # print(listLines)
        
        linesParcour = 0
        documentNumber = 0
        
        document = []
        
        documentList = []
        documentTitle = " "
        text = " "
        writers = " "    
        
    while(linesParcour != len(listLines)):
        line = listLines[linesParcour]

    # extract the file number 
        if (line.startswith(".I")):
            documentNumber = line.split()[1]
            if document != []:
                document.append(documentTitle)
                document.append(text)
                document.append(writers)            
                documentList.append(document)
            document = []
            document.append(documentNumber)
            documentTitle = ""
            text = ""
            writers = ""

    # extract the title 
        if (line.startswith(".T")):
            linesParcour = linesParcour + 1
            while((nltk.re.findall('\.([TWBANX]\n|I d+\n)',listLines[linesParcour]) == []) and (linesParcour < len (listLines) )):
                documentTitle = documentTitle + "" .join(listLines[linesParcour].split("\n")[0].lower())
                linesParcour = linesParcour + 1
            linesParcour = linesParcour - 1     
            
    # extract the text
        if (line.startswith(".W")):
            linesParcour = linesParcour + 1
            while((nltk.re.findall('\.([TWBANX]\n|I d+\n)',listLines[linesParcour]) == []) and (linesParcour < len (listLines) )):
                text = text + "".join(listLines[linesParcour].split("\n")[0].lower())
                linesParcour = linesParcour + 1
            linesParcour = linesParcour - 1
            
    # extract the writers
        if (line.startswith(".A")):
            linesParcour = linesParcour + 1
            while((nltk.re.findall('\.([TWBANX]\n|I [0-9]+\n)',listLines[linesParcour]) == []) and (linesParcour < len (listLines) )):
                writers = writers + "".join(listLines[linesParcour].split("\n")[0].lower())
                linesParcour = linesParcour + 1
            linesParcour = linesParcour - 1     

        linesParcour = linesParcour + 1 
    document.append(documentTitle)
    document.append(text)
    document.append(writers)
    documentList.append(document)

    # for d in documentList[19:20]:
        # print(d)
    
    return documentList[:2]


#fonction calculate the frequency
def calculate_frequency(documentList):

    #create stop words list 
    with open ('data/common_words') as cacm:
        listLines = cacm.readlines()

    stopWordsList=[]
    for l in listLines:
        stopWordsList.append(l.split("\n")[0].lower())
    
    # for l in stopWordsList[:5]:
    #     print(l)

    #tokenizing the texts and calculating the frequancy
    
    wordFrequenctList = {}
    for document in documentList:
        text = ''.join(document[1])
        text = text+"".join(document[2])
        # print(document[2])
        # print(text)
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        tokenizedText = tokenizer.tokenize(text)
        # print(tokenizedText)
        frequences = nltk.FreqDist(sorted(token for token in tokenizedText if token not in stopWordsList))

        # for f in frequences:
        #        print(frequences[f] , " ", f )
        wordFrequenctList[document[0]] =  frequences    

    # friq = wordFrequenctList.keys()
    # for documentNumber in friq:
    #     for word in wordFrequenctList[documentNumber]:
    #         print("{",documentNumber," , " ,word," } ===>" , wordFrequenctList[documentNumber][word])

    return wordFrequenctList   

#calculate the requency of the words 
def create_index_file(wordFrequenctList):
    
    listIndex = {}
    friq = wordFrequenctList.keys()
    for documentNumber in friq:
        for word in wordFrequenctList[documentNumber]:
            listIndex[(documentNumber,word)] = wordFrequenctList[documentNumber][word]
            
    return listIndex
    

#calculate the weights of the words 
def create_indexFile_Weights(wordFrequenctList):
    
    listIndexWeights = {}
    friq = wordFrequenctList.keys()
    for documentNumber in friq:
        max_freq = list(wordFrequenctList[documentNumber].values())[0] 
        for word in wordFrequenctList[documentNumber]:
            freqd = wordFrequenctList[documentNumber][word]
            listIndexWeights[(documentNumber,word)] = ((freqd)/max_freq) * math.log(10)
            print(listIndexWeights[(documentNumber,word)])

    return listIndexWeights

###################################
###################################
#### applying the fonctions########
###################################
###################################

documentList = extract_information()
wordFrequenctList = calculate_frequency(documentList)
create_index_file(wordFrequenctList)
create_indexFile_Weights(wordFrequenctList)