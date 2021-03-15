# back end 
import re 
import nltk
from nltk import text
import numpy as np
import string
import math
from pickle import dump ,load
from nltk.probability import FreqDist 
from server.utils import create_invertedFile ,list_repetition , extract_information ,calculate_frequency ,saveToFile

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
    queryVictor = {}
    for index in range(len(queryWords)):
        word = queryWords[index]
        if word in listWords:
            if listWords.index(word) not in queryVictor.keys():
                 queryVictor[listWords.index(word)] = 0 
            queryVictor[listWords.index(word)] = queryVictor[listWords.index(word)] + 1
  
    ####### calculate sem
    documentList = {}
    if similarityMeasure == "Inner product" :
        for documentNumber in range (len(matrixDoxumentTerm)):
            sommex_y = 0
            sommey_y = 0
            sommex_x = 0
            somme    = 0
 
            for key in queryVictor.keys() :
                sommex_y = sommex_y + queryVictor[key] * matrixDoxumentTerm[documentNumber][key]
                
            if sommex_y != 0 :
                somme = sommex_y
                documentList[documentNumber+1] = somme
            
    elif similarityMeasure == "Sørensen–Dice coefficient":
        for documentNumber in range (len(matrixDoxumentTerm)):
            sommex_y = 0
            sommey_y = 0
            sommex_x = 0
            
            for key in queryVictor.keys():
                sommex_x = sommex_x + queryVictor[key]*queryVictor[key]
                sommey_y = sommey_y + matrixDoxumentTerm[documentNumber][key] * matrixDoxumentTerm[documentNumber][key]
                sommex_y = sommex_y + queryVictor[key]*matrixDoxumentTerm[documentNumber][key]
            if sommex_x + sommey_y > 0 and sommex_y != 0 :
                somme = 2 * sommex_y/(sommex_x + sommey_y)
                documentList[documentNumber+1]= somme
    elif similarityMeasure == "Cosine similarity" : 
        for documentNumber in range (len(matrixDoxumentTerm)):
            sommex_y = 0
            sommey_y = 0
            sommex_x = 0
            somme    = 0
            for key in queryVictor.keys(): 
                sommex_x = sommex_x + queryVictor[key]*queryVictor[key]
                sommey_y = sommey_y + matrixDoxumentTerm[documentNumber][key] * matrixDoxumentTerm[documentNumber][key]
                sommex_y = sommex_y + queryVictor[key]*matrixDoxumentTerm[documentNumber][key]
            if sommex_x * sommey_y > 0 and  sommex_y != 0 :
                somme = sommex_y/math.sqrt(sommex_x * sommey_y)
                documentList[documentNumber+1]= somme

    elif similarityMeasure == "Jaccard index" :
        for documentNumber in range (len(matrixDoxumentTerm)):
            sommex_y = 0
            sommey_y = 0
            sommex_x = 0
            somme    = 0
            for key in queryVictor.keys():
                sommex_x = sommex_x + queryVictor[key]*queryVictor[key]
                sommey_y = sommey_y + matrixDoxumentTerm[documentNumber][key] * matrixDoxumentTerm[documentNumber][key]
                sommex_y = sommex_y + queryVictor[key]*matrixDoxumentTerm[documentNumber][key]
            if sommex_x + sommey_y - sommex_y > 0 and sommex_y != 0 :
                somme = sommex_y/(sommex_x + sommey_y - sommex_y)
                documentList[documentNumber+1]= somme
    
    
    documentListResult = []
    for key,value in documentList.items():
        document = []
        document.append(key)
        document.append(value)
        documentListResult.append(document)
    documentListResult.sort(key = lambda x: x[1] , reverse=True)
    return documentListResult





#evaluation module victorial 
#read query
def readQuery():
    with open ("data/query.text") as query:
        listLines = query.readlines() 
        query = []
        queryList = []
        text=""

        linesParcour = 0
        while(linesParcour != len(listLines)):
            line = listLines[linesParcour]
            if (line.startswith(".I")):
                queryNumber = int(line.split()[1])
                if query != []:
                    query.append(text)
                    queryList.append(query)
                
                query = []
                query.append(queryNumber)

            if (line.startswith(".W")):
                linesParcour = linesParcour + 1
                while((nltk.re.findall('\.([TWBANX]\n|I d+\n)',listLines[linesParcour]) == []) and (linesParcour < len (listLines) )):
                    text = text + "".join(listLines[linesParcour].split("\n")[0].lower())
                    linesParcour = linesParcour + 1
                linesParcour = linesParcour - 1    
            linesParcour = linesParcour + 1

        query.append(text)
        queryList.append(query)        

       
    return queryList


#read qrels

def readQrels():
    with open('data/qrels.text') as qrels :
        listLines = qrels.readlines()

        qrelList = nltk.defaultdict(list)

        for line in listLines:
            splitedLine = line.split()
            qrelList[int(splitedLine[0])].append(int(splitedLine[1]))

          

    return qrelList

#calculer recall

def calculeRecall(queryNumber , resultList , qrelList ):
    documentListResult = []

    for result in resultList:
   
        documentListResult.append(result[0])

    resultSet= set(documentListResult)
    qrelSet  = set(qrelList) 
    print(qrelList)
    intersectionList = list(resultSet.intersection(qrelSet))

    recall = 0.0

    if len(qrelList) != 0:
        recall = (float(len(intersectionList)) / float(len(qrelList)))

    return recall
#calculate Precision
def calculatePrecision(queryNumber , resultList , qrelList ):
    documentsListResult = []

    for result in resultList:
        documentsListResult.append(result[0])

    resultSet= set(documentsListResult)
    qrelSet  = set(qrelList) 

    intersectionList = list(resultSet.intersection(qrelSet))
    precision = 0.0
    
    if len(documentsListResult) != 0:
        precision = (float(len(intersectionList)) / float(len(documentsListResult)))
    
   
    return precision
    
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
    
    
    queryList=readQuery()
    listWords = list(repetitionDict.keys())
    qrelList = readQrels()
   
    for query in queryList:
    
        print("Sørensen–Dice coefficient") 
        
        q=query[1]
        similarityMeasure =  "Sørensen–Dice coefficient"#type de similariy 4
        documentListResult = vectorialModelSearh(q , matrixDoxumentTerm  , similarityMeasure , listWords )
        # print(documentListResult)  
        print("recall of query    :",query[0],calculeRecall(query[0],documentListResult,qrelList[query[0]]))
        print("precision of query    :",query[0],calculatePrecision(query[0],documentListResult,qrelList[query[0]]))
        

        print("Cosine similarity")
        similarityMeasure =  "Cosine similarity"#type de similariy 4
        documentListResult = vectorialModelSearh(q , matrixDoxumentTerm  , similarityMeasure , listWords )
        # print(documentListResult)
        print("recall of query    :",query[0],calculeRecall(query[0],documentListResult,qrelList[query[0]]))
        print("precision of query    :",query[0],calculatePrecision(query[0],documentListResult,qrelList[query[0]]))

        print("Jaccard index")
        similarityMeasure =  "Jaccard index"#type de similariy 4
        documentListResult = vectorialModelSearh(q , matrixDoxumentTerm  , similarityMeasure , listWords )
        # print(documentListResult)
        print("recall of query    :",query[0],calculeRecall(query[0],documentListResult,qrelList[query[0]]))
        print("precision of query    :",query[0],calculatePrecision(query[0],documentListResult,qrelList[query[0]]))

        print("Inner product")
        similarityMeasure =  "Inner product"#type de similariy 4
        documentListResult = vectorialModelSearh(q , matrixDoxumentTerm  , similarityMeasure , listWords )
        # print(documentListResult)
        print("recall of query    :",query[0],calculeRecall(query[0],documentListResult,qrelList[query[0]]))
        print("precision of query    :",query[0],calculatePrecision(query[0],documentListResult,qrelList[query[0]]))

