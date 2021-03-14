import os
import logging
import io
import base64
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.BooleanModel import answareQuery
from server.utils import importFromFile
import nltk



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
def read_item( sent: Optional[str] = None):
    result = answareQuery(sent , doc_index)
    return {"docs": sorted(result)}