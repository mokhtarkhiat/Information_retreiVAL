# back end 
import re 
import nltk
import string
import math
from pickle import dump ,load
from nltk.probability import FreqDist 


#extract information from the file 
def extract_information():
    linesParcour = 0
    documentNumber = 0
    document = []
    documentList = []
    documentTitle = " "
    text = " "
    writers = " " 
    # read the file CACM 

    with open ("data/cacm.all") as cacm:
        listLines = cacm.readlines()
        # print(listLines)   
        
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
    
    return documentList[:20]


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
def create_invertedFile(wordFrequenctList):
    
    invertedFile = {}
    friq = wordFrequenctList.keys()
    for documentNumber in friq:
        for word in wordFrequenctList[documentNumber]:
            invertedFile[(int(documentNumber),word)] = wordFrequenctList[documentNumber][word]
            
    return invertedFile
    
def saveinvertedFile(outputFile,invertedFile) :
    output = open(outputFile, 'wb')
    dump(invertedFile, output, -1)
    output.close()

def importinvertedFile(inputfile) :
    input = open(inputfile, 'rb')
    invertedFile = load(input)
    input.close()
    return invertedFile

#calculate the number of repetition of the word in documents
def list_repetition(wordFrequenctList):
    
    repetitionDict = {}

    for document in wordFrequenctList:
        for word in document.keys():
            if word not in repetitionDict:
                repetitionDict[word] = []

            repetitionDict[word].append(document)    


    return repetitionDict

#calculate the weights of the words 
def create_invertedFile_Weights(wordFrequenctList):
    
    invertedFileWeights = {}
    friq = wordFrequenctList.keys()
    for documentNumber in friq:
        max_freq = list(wordFrequenctList[documentNumber].values())[0] 
        for word in wordFrequenctList[documentNumber]:
            freqd = wordFrequenctList[documentNumber][word]
            invertedFileWeights[(documentNumber,word)] = ((freqd)/max_freq) * math.log(10)
            # print(invertedFileWeights[(documentNumber,word)])

    return invertedFileWeights

def saveInvertedFileWeights(outputFile,invertedFileWeights) :
    output = open(outputFile, 'wb')
    dump(invertedFileWeights, output, -1)
    output.close()

def importInvertedFileWeights(inputfileWeights) :
    input = open(inputfileWeights, 'rb')
    invertedFileWeights = load(input)
    input.close()
    return invertedFileWeights

###################################
###################################
#### applying the fonctions########
###################################
###################################
if __name__ == '__main__':
    documentList = extract_information()
    wordFrequenctList = calculate_frequency(documentList)

    # invertedFile = create_invertedFile(wordFrequenctList)
    # saveInvertedFile("data/invertedFile.pkl",invertedFile)

    # invertedFile_weights =create_invertedFile_Weights(wordFrequenctList)
    # saveinvertedFileWeights("data/invertedFileWeights.pkl",invertedFileWeights)


    # print(wordFrequenctList)