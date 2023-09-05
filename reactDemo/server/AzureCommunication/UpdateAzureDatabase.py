from typing import List, Dict, Any, Tuple
import json
from config import headers, knowledgeBaseUrl, knowledgeBaseQueryUrl
import requests

'''
This file handles communication between the backend flask server and the azure Knoweledge Base
'''


def getAllQuestionsAndAnswersFromAzure(source: str = "") -> Dict[str, Any]:
    # load all questions and answers into a dictionary from the azure knowledge
    r = requests.get(url=knowledgeBaseUrl + f"&source={source}", headers=headers)
    j = json.loads(r.text)
    return j


def addQuestionsAzure(ids: List[int], questions: List[str], answers: List[str], sources: List[str], ratings:List[int]) -> requests.models.Response:
    # add questions to the azure kb
    upload = []

    for id, question, answer, source, rating in zip(ids, questions, answers, sources,ratings):
        data = {
            "op": "add",
            "value": {
                "id": id,
                "answer": f"{answer}",
                "source": f"{source}",
                "questions": [
                    f"{question[0]}"
                ],
                "metadata": {
                    "topic": "chatgpt",
                    "rating":rating
                }
            }
        }
        upload.append(data)

    datajs = json.dumps(upload)
    print(datajs)

    r = requests.patch(url=knowledgeBaseUrl, headers=headers, data=datajs)
    print(f"Adding Questions Status: {r.status_code}")
    return r


def UpdateQuestionsAzure(ids: List[int], questions: List[str]):
    # update questions in azure kb
    upload = []

    for id, q in zip(ids, questions):
        data = {
            "op": "replace",
            "value": {
                "id": id
            }
        }
        # if a is not None:
        #     data["value"]["answer"] = f"{a}"  # type:ignore
        # if s is not None:
        #     data["value"]["source"] = f"{s}"  # type:ignore
        if q is not None:
            data["value"]["questions"] = [] # type:ignore
            for q1 in q:
                data["value"]["questions"].append(f"{q1}")  # type:ignore
        # if t is not None:
        #     data["value"]["metadata"] = {}  # type:ignore
        #     for t1 in t:
        #         data["value"]["metadata"][t1[0]] = t1[1]  # type:ignore

        upload.append(data)

    datajs = json.dumps(upload)

    r = requests.patch(url=knowledgeBaseUrl, headers=headers, data=datajs)
    print(f"Updating Questions Status: {r.status_code}")
    return r



def DeleteQuestionsAzure(ids: List[int]):
    # remove questions from azure kb
    upload = []

    for id in ids:
        data = {
            "op": "delete",
            "value": {
                "id": id
            }
        }
        upload.append(data)

    datajs = json.dumps(upload)

    r = requests.patch(url=knowledgeBaseUrl, headers=headers, data=datajs)

    print(f"Deleting Questions Status: {r.status_code}")
    return r


def QuerryAzure(question, context:Tuple[int, str]= None, source:str= None, filters=None):

    # structure question in data json format
    data = {
        "question":question,
        "top":3,
        "confidenceScoreThreshold": 0.2,
        "includeUnstructuredSources": True,
        "rankerType": "Default",
    }

    # determine context of question
    if context is not None and len(context) > 0:
        data["context"] = {
        "previousUserQuery":context[0],
        "previousQnaId":context[1]
        }

    # assign filters
    data["filters"] = {}
    if filters is not None and len(filters)> 0:
        data["filters"]["metadataFilter"] ={
            "logicalOperation":"AND",
            "metadata":[],
        }
        for f in filters:
            md = {
            "key":f[0],
            "value":f[1]
            }
            data["filters"]["metadataFilter"]["metadata"].append(md) 

    if source:
        data["filters"]["sourceFilter"] = []
        data["filters"]["logicalOperation"] = "AND"
        data["filters"]["sourceFilter"].append(source)

    datajs = json.dumps(data)
    print(datajs)
    r = requests.post(url=knowledgeBaseQueryUrl, headers=headers, data=datajs)
    j =json.loads(r.text)
    return j


if __name__ == "__main__":
    print(QuerryAzure("What is chatGPT?", source="ChatGPT"))
