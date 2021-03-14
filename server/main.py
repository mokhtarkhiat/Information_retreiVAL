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



######## vectorial search 
# preparation (creat the matrix)
def preparationVectorialSearch(repetitionDict,invertedFile,numberDocuments):
    
    matrixDoxumentTerm = np.zeros( ( numberDocuments,len(repetitionDict.keys()) ) )
    wordIndexInRepetition = 0
    
    for word,documentCollection in repetitionDict.items():
        for documentNumber in documentCollection: 

            matrixDoxumentTerm[documentNumber-1][wordIndexInRepetition] = invertedFile[ (word, documentNumber ) ]

        wordIndexInRepetition = wordIndexInRepetition + 1

    # for j in matrixDoxumentTerm.:
    
    return matrixDoxumentTerm
#search
def vectorialModelSearh(Query , matrixDoxumentTerm , similarityMeasure ,listWords ):
    
    with open ('data/common_words') as common_word:
        listLines = common_word.readlines()
    stopWordsList=[]
    for l in listLines:
        stopWordsList.append(l.split("\n")[0].lower())

       
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    queryAllWords = tokenizer.tokenize(Query)
    queryWords = list(sorted(token.lower() for token in queryAllWords if token not in stopWordsList))
    
    ####### query victor
    queryVictor = np.zeros(len(listWords))
    for index in range(len(queryWords)):
        word = queryWords[index]
        
        if word in listWords:
            
            queryVictor[listWords.index(word)] = queryVictor[listWords.index(word)] + 1
  
    ####### calculate sem
    documentList = {}
    if similarityMeasure == "Inner product" :
        for documentNumber in range (len(matrixDoxumentTerm)):
            sommex_y = 0
            sommey_y = 0
            sommex_x = 0
            somme    = 0
           
            for word in range (len(queryVictor)) :
                sommex_y = sommex_y + queryVictor[word] * matrixDoxumentTerm[documentNumber][word]
            
            if sommex_y != 0 :
                somme = sommex_y
                documentList[documentNumber+1]= somme
            
    elif similarityMeasure == "Sørensen–Dice coefficient":
        for documentNumber in range (len(matrixDoxumentTerm)):
            sommex_y = 0
            sommey_y = 0
            sommex_x = 0
            somme    = 0
            for word in range (len(queryVictor)) :
                sommex_x = sommex_x + queryVictor[word]*queryVictor[word]
                sommey_y = sommey_y + matrixDoxumentTerm[documentNumber][word] * matrixDoxumentTerm[documentNumber][word]
                sommex_y = sommex_y + queryVictor[word]*matrixDoxumentTerm[documentNumber][word]
            if sommex_x + sommey_y > 0 and sommex_y != 0 :
                somme = 2 * sommex_y/(sommex_x + sommey_y)
                documentList[documentNumber+1]= somme
    elif similarityMeasure == "Cosine similarity" : 
        for documentNumber in range (len(matrixDoxumentTerm)):
            sommex_y = 0
            sommey_y = 0
            sommex_x = 0
            somme    = 0
            for word in range (len(queryVictor)):
                sommex_x = sommex_x + queryVictor[word]*queryVictor[word]
                sommey_y = sommey_y + matrixDoxumentTerm[documentNumber][word] * matrixDoxumentTerm[documentNumber][word]
                sommex_y = sommex_y + queryVictor[word]*matrixDoxumentTerm[documentNumber][word]
            if sommex_x * sommey_y > 0 and  sommex_y != 0 :
                somme = sommex_y/math.sqrt(sommex_x * sommey_y)
                documentList[documentNumber+1]= somme

    elif similarityMeasure == "Jaccard index" :
        for documentNumber in range (len(matrixDoxumentTerm)):
            sommex_y = 0
            sommey_y = 0
            sommex_x = 0
            somme    = 0
            for word in range (len(queryVictor)) :
                sommex_x = sommex_x + queryVictor[word]*queryVictor[word]
                sommey_y = sommey_y + matrixDoxumentTerm[documentNumber][word] * matrixDoxumentTerm[documentNumber][word]
                sommex_y = sommex_y + queryVictor[word]*matrixDoxumentTerm[documentNumber][word]
            if sommex_x + sommey_y - sommex_y > 0 and sommex_y != 0 :
                somme = sommex_y/(sommex_x + sommey_y - sommex_y)
                documentList[documentNumber+1]= somme
    
    
    documentListResult = list(documentList.keys())
    documentListResult = sorted(documentListResult)
    return documentListResult



#evaluation module victorial 
#calculer recall

def calculeRecall():

    return
#calculate Precision
def calculatePrecision():
    
    return
    
###################################
###################################
#### applying the fonctions########
###################################
###################################
if __name__ == '__main__':
    documentList = extract_information()
    wordFrequenctList = calculate_frequency(documentList)

    
    invertedFile = create_invertedFile(wordFrequenctList)
    # saveInvertedFile("data/invertedFile.pkl",invertedFile)
    
    
    repetitionDict = list_repetition(wordFrequenctList)
    # invertedFile_weights =createInvertedFileWeights(wordFrequenctList,repetitionDict)
    # saveInvertedFileWeights("data/invertedFileWeights.pkl",invertedFile_weights)
    matrixDoxumentTerm = preparationVectorialSearch(repetitionDict,invertedFile,len(documentList) )
    
    query = 'Dictionary construction and accessing methods for fast retrieval of words or lexical items or morphologically related information. Hashing or indexing methods are usually applied to English spelling or natural language problems.'
    
    similarityMeasure =  "Sørensen–Dice coefficient"#type de similariy 4
    listWords = list(repetitionDict.keys())
    
    documentListResult = vectorialModelSearh(query , matrixDoxumentTerm  , similarityMeasure , listWords )
    print(len(documentListResult))
    
    
    similarityMeasure =  "Cosine similarity"#type de similariy 4
    documentListResult = vectorialModelSearh(query , matrixDoxumentTerm  , similarityMeasure , listWords )
    print(len(documentListResult))
    
    similarityMeasure =  "Jaccard index"#type de similariy 4
    documentListResult = vectorialModelSearh(query , matrixDoxumentTerm  , similarityMeasure , listWords )
    print(len(documentListResult))

    similarityMeasure =  "Inner product"#type de similariy 4
    documentListResult = vectorialModelSearh(query , matrixDoxumentTerm  , similarityMeasure , listWords )
    print(len(documentListResult))
    
    
    


    # invertedFile = create_invertedFile(wordFrequenctList)
    # saveToFile("data/invertedFile.pkl",invertedFile)

    # invertedFile_weights = createInvertedFileWeights(wordFrequenctList)
    # saveToFile("data/invertedFileWeights.pkl",invertedFile_weights)

    # list_repetition(wordFrequenctList)
    saveToFile('data/repetitionList.pkl' , list_repetition(wordFrequenctList))
    # print(wordFrequenctList)