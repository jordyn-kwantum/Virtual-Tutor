from distutils.command.upload import upload
import requests
import json
import random
from typing import List, Dict
# import info as i
import pickle
import os
import time

from typing import List, Set, Dict, Tuple, Optional

headers = {
    "projectName":"SquadDemo ",
    "api-version":"2021-10-01",
    "deploymentName":"production",
    "Ocp-Apim-Subscription-Key":"6b4cedc723344e79852b272530bd2bb0",
    "Content-Type":"application/json"
}


def getQnA(source = ""):
    if source:
        headers["source"] = source
    print(headers)
    r = requests.get(url = f"https://cogservtextanalytics1.cognitiveservices.azure.com/language/query-knowledgebases/projects/SquadDemo/qnas?api-version=2021-10-01&source={source}", headers = headers)
    j = json.loads(r.text)
    return j

def addTags():
    titles = []
    for filename in os.listdir("pdfs"):
        if filename.endswith(".pdf"):
            titles.append(filename)
    print(titles)

    count = 0

    r = requests.get(url = f"https://cogservtextanalytics1.cognitiveservices.azure.com/language/query-knowledgebases/projects/SquadDemo/qnas?api-version=2021-10-01", headers = headers)
    j = json.loads(r.text)

    newVersion = []
    for elem in j["value"]:
        data = {
            "op": "replace",
            "value": {
                "id":elem["id"],
                "answer":elem["answer"],
                "source":elem["source"],
                "questions":elem["questions"],
                "metadata":{
                    "title":elem["source"][:-4].replace(" ", "_")
                },
            }}
        if "dialog" in elem:
            data["value"]["dialog"] = elem["dialog"] 


        newVersion.append(data)
    datajs = json.dumps(newVersion)
    r = requests.patch(url = f"https://cogservtextanalytics1.cognitiveservices.azure.com/language/query-knowledgebases/projects/SquadDemo/qnas?api-version=2021-10-01&", headers = headers, data=datajs)
    return r


def updateQuestions(id:List[int], questions:List[str], answer:List[str], source:List[str], tags:List[Tuple[str, str]]=None):
    upload =[]

    for i in range(len(id)):
        data = {
            "op":"replace",
            "value":{
                "id" : id[i],
                "answer" : answer[i],
                "source" : source[i],
                "questions": [questions[i]],
                "metadata":{},
            },
        }

        if tags:
            for tag in tags:
                data["value"]["metadata"][tag[0]] = tag[1] #type: ignore

        upload.append(data)
    headers = {
        "projectName":"SquadDemo ",
        "api-version":"2021-10-01",
        "deploymentName":"production",
        "Ocp-Apim-Subscription-Key":"6b4cedc723344e79852b272530bd2bb0",
        "Content-Type":"application/json"
    }


    datajs = json.dumps(upload)
    r = requests.patch(url = f"https://cogservtextanalytics1.cognitiveservices.azure.com/language/query-knowledgebases/projects/SquadDemo/qnas?api-version=2021-10-01&", headers = headers, data=datajs)
    print(r)
    return r



def updateQuestion(id:int,question:str, answer:str,source:str, tags:List[Tuple[str, str]]=None):
    upload = []

    data = {
        "op":"replace",
        "value":{
        "id": id,
        "answer": f"{answer}",
        "source": f"{source}",
        "questions":[
        f"{question}"
        ],
        "metadata":{}
        }
    }
    headers = {
        "projectName":"SquadDemo ",
        "api-version":"2021-10-01",
        "deploymentName":"production",
        "Ocp-Apim-Subscription-Key":"6b4cedc723344e79852b272530bd2bb0",
        "Content-Type":"application/json"
    }

    if not( tags is None):
        for tag in tags:
            data["value"]["metadata"][tag[0]] = tag[1] #type: ignore

    upload.append(data)

    datajs = json.dumps(upload)
    # print(datajs)

    # r = requests.patch(url = f"https://westus2.api.cognitive.microsoft.com/language/query-knowledgebases/projects/{i.projectName}/qnas?api-version=2021-10-01", headers = headers, data=datajs)
    r = requests.patch(url = f"https://cogservtextanalytics1.cognitiveservices.azure.com/language/query-knowledgebases/projects/SquadDemo/qnas?api-version=2021-10-01&", headers = headers, data=datajs)
    print(r)
    return r

def addQuestion(question:str, answer:str,source:str, tags:List[Tuple[str, str]]=None):
    upload = []

    data = {
        "op":"add",
        "value":{
        "answer": f"{answer}",
        "source": f"{source}",
        "questions":[
        f"{question}"
        ],
        "metadata":{}
        }
    }
    headers = {
        "projectName":"SquadDemo ",
        "api-version":"2021-10-01",
        "deploymentName":"production",
        "Ocp-Apim-Subscription-Key":"6b4cedc723344e79852b272530bd2bb0",
        "Content-Type":"application/json"
    }

    if not( tags is None):
        if "metadata" not in data:
            data["metadata"] = {}
        for tag in tags:
            data["metadata"][tag[0]] = tag[1] #type: ignore

    upload.append(data)

    datajs = json.dumps(upload)

    r = requests.patch(url = f"https://cogservtextanalytics1.cognitiveservices.azure.com/language/query-knowledgebases/projects/SquadDemo/qnas?api-version=2021-10-01&", headers = headers, data=datajs)

    return r

def addSuggestion(questions, suggestions):
    upload = []
    for j, elem in enumerate(questions):
        # print(elem)
        dataelem = {
        "op": "replace",
        "value": {
        "id": elem['answers'][0]['id'],
        "answer": elem['answers'][0]['answer'],
        "source": elem['answers'][0]["source"],
        "questions": [
        elem['answers'][0]["questions"][0]
        ],
        "metadata": elem['answers'][0]["metadata"],
        "dialog": elem['answers'][0]["dialog"],
        "activeLearningSuggestions": [{
        "clusterHead": suggestions[j],
        "suggestedQuestions": [{
        "question": suggestions[j],
        "userSuggestedCount": 1,
        "autoSuggestedCount": 0
        }]
        }]
        }
        }
        upload.append(dataelem)

    datajs = json.dumps(upload)

    r = requests.patch(url = f"https://cogservtextanalytics1.cognitiveservices.azure.com/language/query-knowledgebases/projects/SquadDemo/qnas?api-version=2021-10-01&", headers = headers, data=datajs)

    return r


def addFeedback(students, questions, suggestions):
    upload = {"records":[]}
    for j, elem in enumerate(questions):
        # print(elem)
        dataelem = {
        "userId":students[j],
        "qnaId":elem['answers'][0]['id'],
        "userQuestion":suggestions[j]
        }
        upload["records"].append(dataelem)

    datajs = json.dumps(upload)
    r = requests.post(url = f"https://cogservtextanalytics1.cognitiveservices.azure.com/language/query-knowledgebases/projects/SquadDemo/feedback?api-version=2021-10-01&", headers = headers, data=datajs)

    return r


if __name__ == "__main__":
    questions = getQnA("PrimeMinisterQuestions.pdf")
    print(questions["value"])  
    ids = []
    qs = []
    answers = []
    sources = []
    tags = [("assignment","PrimeMinister")]
    for q in questions["value"]:
        ids.append(q['id'])
        qs.append(q['questions'][0])
        answers.append(q["answer"])
        sources.append(q["source"])
        
    updateQuestions(ids,qs, answers, sources, tags)
