import os
import logging
import io
import base64
from operator import itemgetter
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.BooleanModel import answareQuery
from server.utils import importFromFile , extract_information
from server.vectorialSearch import preparationVectorialSearch,vectorialModelSearh
import nltk


<<<<<<< HEAD
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
    
    
    documentListResult = list(documentList.items())
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
    wordFrequenctList = calcul<ate_frequency(documentList)

    
    invertedFile = create_invertedFile(wordFrequenctList)
    # saveInvertedFile("data/invertedFile.pkl",invertedFile)
    
    
    repetitionDict = list_repetition(wordFrequenctList)
    # invertedFile_weights =createInvertedFileWeights(wordFrequenctList,repetitionDict)
    # saveInvertedFileWeights("data/invertedFileWeights.pkl",invertedFile_weights)
    matrixDoxumentTerm = preparationVectorialSearch(repetitionDict,invertedFile,len(documentList) )
    
    query = 'Interested in articles on robotics, motion planning particularly the geometric and combinatorial aspects.  We are not interested in the dynamics of arm motion. '
    
    similarityMeasure =  "Sørensen–Dice coefficient"#type de similariy 4
    listWords = list(repetitionDict.keys())
    
    # documentListResult = vectorialModelSearh(query , matrixDoxumentTerm  , similarityMeasure , listWords )
    # print(documentListResult)
    
    
    similarityMeasure =  "Cosine similarity"#type de similariy 4
    documentListResult = vectorialModelSearh(query , matrixDoxumentTerm  , similarityMeasure , listWords )
    print(documentListResult)
    
    # similarityMeasure =  "Jaccard index"#type de similariy 4
    # documentListResult = vectorialModelSearh(query , matrixDoxumentTerm  , similarityMeasure , listWords )
    # print(documentListResult)
=======
documentList = extract_information()
invertedfile : dict = importFromFile('data/invertedFile.pkl')
doc_index : dict = importFromFile('data/repetitionList.pkl')
>>>>>>> 766f4af39900aeac30fd1fb3c34129c70d58b04f



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"rules": "nothing here"}


@app.get("/booleansearch")
def booleansearch( sent: Optional[str] = None):
    result = answareQuery(sent , doc_index)
    return {"docs": sorted(result)}


#type de similariy 4
simi_types = {
    0:"Sørensen–Dice coefficient",
    1:"Cosine similarity",
    2:"Jaccard index",
    3:"Inner product",
}

@app.get("/vectsearch")
def vectsearch(sent: Optional[str] = None ,type: Optional[int] = None):
    print(documentList.__len__())
    matrixDoxumentTerm = preparationVectorialSearch(doc_index,invertedfile,len(documentList) )

    similarityMeasure =  simi_types[type]
    listWords = list(doc_index.keys())
    documentListResult = vectorialModelSearh(sent , matrixDoxumentTerm  , similarityMeasure , listWords )

    return {"docs": sorted(documentListResult , key=lambda x : x[1] , reverse=True)[:20]}