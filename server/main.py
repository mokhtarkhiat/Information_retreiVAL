# back end 
import re 
import nltk
import string


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

######      TOKNIZING the texts and removing the stop words 


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

friq = wordFrequenctList.items()
for k in friq:
    print(k)
       
#     text_words = nltk.word_tokenize(list_texts[j])
        
#     dict_occu = {}
#     word_index = []   
 
#     while text_words:
#        print(text_words)
#        word = text_words.pop(0)
#        i = 0
#        try:
#             while True:
#               i = i+1
#               text_words.remove(word)
#        except ValueError:
#              pass    
#        dict_occu[word] = i
#     word_index.append(sorted(dict_occu))
#     text_index[j+1] = word_index 
    
# print(text_index)    
# identification of the duc
    
    # tokenizing 
    
    # delet the unnececery words 

# save the results into a list  

# creating hhe inverse file

# boolean search 

# vectoriel search 

