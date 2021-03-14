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


documentList = extract_information()
invertedfile : dict = importFromFile('data/invertedFile.pkl')
doc_index : dict = importFromFile('data/repetitionList.pkl')



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