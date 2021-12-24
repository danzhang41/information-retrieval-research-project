from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models import KeyedVectors


def process():
    documents = []
    file = open('document_list.txt', 'r', encoding="utf-8")

    for line in file:
        words = line.split(" ")
        document_words = []
        for word in words:
            document_words.append(word)
        documents.append(document_words)
    return documents

def train(documents):
    model = Word2Vec(documents, vector_size=50, window=5, min_count=2,workers=10, sg=1)
    model.train(documents, total_examples=len(documents), epochs=10)
    model.wv.save("model.wordvectors")
    

def getEmbeddings():
    wv = KeyedVectors.load("model.wordvectors", mmap='r')
    file = open('word_count.txt', 'r', encoding="utf-8")
    out = open('word2vec_embedding.txt', 'w', encoding="utf-8")
    for line in file:
        word_and_count = line.split(" ")
        word = word_and_count[0]
        try:
            vector = wv[word]
            out.write(word + " ")
            for num in vector:
                out.write(str(num)+ " ")
            out.write("\n")
        except:
            continue

documents = process()
train(documents)
getEmbeddings()
