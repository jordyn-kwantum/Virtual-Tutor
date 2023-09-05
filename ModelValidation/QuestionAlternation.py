import random
import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet
import pickle


Q = "What century did the Normans first gain their separate identity"
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')

def swapwords(qarr):
    retArr = []
    for i in range(2):
        a = random.randint(0, len(qarr)-1)
        b = random.randint(0, len(qarr)-1)
        while b == a and len(qarr)>1:
            b = random.randint(0, len(qarr)-1)
        newArr = qarr.copy()
        newArr[a], newArr[b] = newArr[b],newArr[a]
        retArr.append(newArr)
    return retArr

def removeWords(qarr):
    retArr = []
    for i, word in enumerate(qarr):
        if word[1].startswith("NN") or word[1].startswith("VB") or word[1].startswith("WP"):
            continue
        newArr = qarr.copy()
        del newArr[i]
        retArr.append(newArr)

    return retArr


def AddSynonyms(qarr):
    a = random.randint(0, len(qarr)-1)
    # count = 0
    # while not( qarr[a][1].startswith("NN") or qarr[a][1].startswith("VB") or qarr[a][1].startswith("WP")):
    #     a =random.randint(0, len(qarr)-1)
    #     count +=1
    #     if count >= 10:
    #         return qarr
    try:
        syn = random.choice(random.choice(wordnet.synsets(qarr[a][0])).lemmas()).name()
    except:
        syn = qarr[a][0]
    newArr = qarr.copy()
    newArr[a] = (syn, qarr[a][1])
    return newArr

def alternativeQuestion(question:str):
    posQ = nltk.pos_tag(word_tokenize(Q))
    questionarray = []
    questionarray.append(posQ)
    for i in range(10):
        questionarray.append(AddSynonyms(posQ))

    for i in range(len(questionarray)):
        questionarray += swapwords(questionarray[i])

    for i in range(len(questionarray)):
        questionarray += removeWords(questionarray[i])

    for i in range(int(len(questionarray)/2), len(questionarray)):
        questionarray += removeWords(questionarray[i])

    questions = list(map(lambda x: " ".join([i[0] for i in x]), questionarray))

    return questions

questions = alternativeQuestion(Q)

with open("questions2.txt", 'w') as f:
    for q in questions:
        f.writelines(q + "\n")
