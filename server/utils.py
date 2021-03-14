# back end 
import re 
import nltk
import numpy as np
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
    

    return documentList


#fonction calculate the frequency
def calculate_frequency(documentList):

    #create stop words list 
    with open ('data/common_words') as cacm:
        listLines = cacm.readlines()

    stopWordsList=[]
    for l in listLines:
        stopWordsList.append(l.split("\n")[0].lower())
    #tokenizing the texts and calculating the frequancy
    
    wordFrequenctList = {}
    for document in documentList:
        text = ''.join(document[1])
        text = text+"".join(document[2])
        tokenizer = nltk.RegexpTokenizer(r"\w+")
        tokenizedText = tokenizer.tokenize(text)
        frequences = nltk.FreqDist(sorted(token for token in tokenizedText if token not in stopWordsList))
        wordFrequenctList[document[0]] =  frequences    
    return wordFrequenctList  

#calculate the requency of the words 
def create_invertedFile(wordFrequenctList):
    
    invertedFile = {}
    friq = wordFrequenctList.keys()
    for documentNumber in friq:
        for word in wordFrequenctList[documentNumber]:
            invertedFile[(word,int(documentNumber))] = wordFrequenctList[documentNumber][word]
            
    return invertedFile
    
def saveToFile(outputFile,obj) :
    output = open(outputFile, 'wb')
    dump(obj, output, -1)
    output.close()

def importFromFile(inputfile) :
    input = open(inputfile, 'rb')
    invertedFile = load(input)
    input.close()
    return invertedFile

#calculate the number of repetition of the word in documents
def list_repetition(wordFrequenctList):
    
    repetitionDict = {}

    for key,value in wordFrequenctList.items():
        for word in value:
            if word not in repetitionDict:
                repetitionDict[word] = []

            repetitionDict[word].append(int(key))    
       

    return repetitionDict

# def satDocsForWord(wordFrequenctList , word):


    

#calculate the weights of the words 
def createInvertedFileWeights(wordFrequenctList,repetitionDict):
    numberOfWords = len(repetitionDict.keys())
    invertedFileWeights = {}
    friq = wordFrequenctList.keys()
    for documentNumber in friq:
        max_freq = list(wordFrequenctList[documentNumber].values())[0] 
        for word in wordFrequenctList[documentNumber]:
            freqd = wordFrequenctList[documentNumber][word]
            numberRepetitionWord = len(repetitionDict[word])
            invertedFileWeights[(word,int(documentNumber))] = ((freqd)/max_freq) * math.log10((numberOfWords/numberRepetitionWord)+1)
            # print(invertedFileWeights[(documentNumber,word)])
    
    
    print(invertedFileWeights)
    return invertedFileWeights



if __name__ == '__main__':

    documentList = extract_information()
    wordFrequenctList = calculate_frequency(documentList)

    
    invertedFile = create_invertedFile(wordFrequenctList)
    # saveInvertedFile("data/invertedFile.pkl",invertedFile)
    
    
    repetitionDict = list_repetition(wordFrequenctList)

    # invertedFile = create_invertedFile(wordFrequenctList)
    # saveToFile("data/invertedFile.pkl",invertedFile)

    # invertedFile_weights = createInvertedFileWeights(wordFrequenctList)
    # saveToFile("data/invertedFileWeights.pkl",invertedFile_weights)

    # list_repetition(wordFrequenctList)
    saveToFile('data/repetitionList.pkl' , list_repetition(wordFrequenctList))
    # print(wordFrequenctList)