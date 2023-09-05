from unicodedata import name
import requests
import json
import random
from typing import List, Dict, Tuple
import python.info as i
import pickle
import nltk
import heapq
import re

headers = {
        "Ocp-Apim-Subscription-Key":"6b4cedc723344e79852b272530bd2bb0",
        "Content-Type":"application/json"
    }

def getLanguage(text:str):
    global headers
    data = {
        "kind": "LanguageDetection",
        "parameters": {
            "modelVersion": "latest"
        },
        "analysisInput":{
        "documents":[
            {
                "id":"1",
                "text": text
            }
        ]
    }
    }

    datajs = json.dumps(data)
    r = requests.post(url = "https://cogservtextanalytics1.cognitiveservices.azure.com/language/:analyze-text?api-version=2022-05-01", headers = headers, data = datajs)
    response = json.loads(r.text)
    language = ""
    try:
        language = response["results"]["documents"][0]["detectedLanguage"]
    except:
        return language
    return language

def summarize(text, detail = 10):
    stopwords = nltk.corpus.stopwords.words('english')

    sentence_list = nltk.sent_tokenize(text)
    formatted_text = re.sub('[^a-zA-Z]', ' ', text )
    formatted_text = re.sub(r'\s+', ' ', formatted_text)

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    summary_sentences = heapq.nlargest(detail, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary

def summarize_request(id, conversation):
    data = {
    "displayName":f"Summarize Conversation of Student {id}",
    "analysisInput":{
        "conversations":[
        {
            "modality": "text",
            "id":f"conversation_{id}",
            "language":"en",
            "conversationItems": []
        }
        ]
    },
    "tasks":[
    {
        "taskname": f"analyze {id}",
        "kind": "ConversationalSummarizationTask",
        "parameters": {
            "modelVersion": "2022-05-15-preview",
            "summaryAspects": [
            "Issue",
            "Resolution"
            ]
            }
    }
    ]
    }

    for elem in conversation:
        count = 0
        block = {
            "text":elem[1],
            "id":f"{count}",
            "role":"Student",
            "participantId":f"student_{id}"
        }
        count +=1
        block2 = {
            "text":elem[2]["answers"][0]["questions"][0],
            "id":f"{count}",
            "role":"Bot",
            "participantId":f"bot"
        }
        data["analysisInput"]["conversations"][0]["conversationItems"].append(block)
        data["analysisInput"]["conversations"][0]["conversationItems"].append(block2)

    datajs = json.dumps(data)
    headers = {
        "Ocp-Apim-Subscription-Key":"6b4cedc723344e79852b272530bd2bb0",
        "Content-Type":"application/json"
    }

    print(datajs)

    r = requests.post(url = "https://cogservtextanalytics1.cognitiveservices.azure.com/language/analyze-conversations/jobs?api-version=2022-05-15-preview", headers = headers, data = datajs)
    print(r)
    print(r.headers)
    location = r.headers["operation-location"]

    r2 = requests.get(url=location, headers = i.headers)
    j = json.loads(r.text)
    return j


if __name__ == "__main__":
    getLanguage("This is an english sentence")