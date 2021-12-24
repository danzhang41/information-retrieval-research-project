import os
import string
import re
import string
import gensim.downloader as api
import nltk

word_count = dict()
documents = []
#out = open('document_list.txt', 'w', encoding="utf-8")
def findAllTxt():
        
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith(".txt") and file != 'document_list.txt':
                process(os.path.join(root, file))
                #word2vec_processing(os.path.join(root, file))
def process(fileName):
    document_words = []
    f = open(fileName, "r", encoding="utf8", errors = "ignore") # , 
    for sentence in f:
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        sentence = normalize(sentence)
        tokens = sentence.split(" ")
        # Iterate over each word in line
        for word in tokens:
            if(not word or word.isnumeric()):
                continue
            # Check if the word is already in dictionary
            if word in word_count:
                # Increment count of word by 1
                word_count[word] = word_count[word] + 1
            else:
                # Add the word to dictionary with count 1
                word_count[word] = 1
            #add it to the document list
def normalize(text):
    text = text.replace('\n'," ")
    text = text.replace('“', " ")
    text = text.replace('”', " ")
    text = text.lower()
    text = text.strip()
    text = text.encode('utf-8').decode('utf-8', 'ignore')
    print(text)
    return text
     

                
def outputWordCount():
    file = open('word_count.txt', 'w', encoding="utf-8")
    for key, value in word_count.items():
        
        newStr = key.strip() + " " + str(value)
        file.write(newStr + "\n")
    file.close()

findAllTxt()
outputWordCount()

