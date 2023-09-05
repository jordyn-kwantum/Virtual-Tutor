from typing import List, Tuple
from Database.models import Tag, Question, QApair, db
from AzureCommunication.UpdateAzureDatabase import addQuestionsAzure, UpdateQuestionsAzure, DeleteQuestionsAzure, getAllQuestionsAndAnswersFromAzure, QuerryAzure
from config import SOURCE
from QuestionsAndAnswers.currentQuestions import localQuestion
from Language.translation import Translator
import json
from config import headers, knowledgeBaseUrl, knowledgeBaseQueryUrl
import requests

'''
This file is responsible for adding, updating and removing questions from the local database.
'''

startingId = 0 


def addAllQuestions(source:str = "", translator:Translator = None):
    global startingId
    qas = getAllQuestionsAndAnswersFromAzure(source)
    qas = qas["value"]
    maxid = 0
    for elem in qas:
        if elem["id"] > maxid:
            maxid = elem["id"]
        if translator:
            pair = QApair(answer = translator.translate([elem["answer"]])[0], source = elem["source"], context="", id = elem["id"])
        else:
            pair = QApair(answer = elem["answer"], source = elem["source"], context="", id = elem["id"])
        for q in elem["questions"]:
            if translator:
                qnew = Question(question = translator.translate([q])[0])
            else:
                qnew = Question(question = q)
            pair.questions.append(qnew)
            db.session.add(qnew)
        for key, value in elem["metadata"].items():
            if key == "rating":
                pair.rating = int(value)
            else:
                t = Tag(key = key, value = value)
                pair.tags.append(t)
                db.session.add(t)
        db.session.add(pair)
    db.session.commit()

    startingId = maxid + 1


def deleteAllQuestions(source:str = SOURCE):
    pairs = QApair.query.all()
    ids = []
    for pair in pairs:
        ids.append(pair.id)
    DeleteQuestions(ids, Azure=True)

def addKBQuestions(filepath:str):
    upload = []
    id = 3000
    with open(filepath, 'r') as fp:
        questions = []
        answer = ""
        for line in fp.readlines():
            if line == "\n":
                if len (questions) == 0:continue
                data = {
                    "op": "add",
                    "value": {
                        "id": id,
                        "answer": answer.strip(),
                        "source": SOURCE,
                        "questions": [q.strip() for q in questions],
                        "metadata": {
                            "topic": "chatgpt",
                            "rating":3
                        }
                        }
                }
                id += 1
                questions = []
                answer = ""
                upload.append(data)

            if line.startswith("Q:"):
                questions.append(line[2:])
            if line.startswith("A"):
                answer = line[2:]
    
    upload = json.dumps(upload)
    # print(upload)

    r = requests.patch(url=knowledgeBaseUrl, headers=headers, data=upload)
    if r.status_code != 202:
        print(r.json())
    print(f"Adding Questions status: {r.status_code}")
    return r


def addLocalQuestions(questions:List[str], answers:List[str], Current:List[localQuestion], ratings:List[int]=None, addtoDB=False, translatorToEn:Translator=None,  translatorToFin:Translator=None):
    global startingId
    if len(questions) is not len(answers):
        raise ValueError("Questions and answers must have the same length")

    for i, (q, a) in enumerate(zip(questions, answers)):
        
        lq = localQuestion(id = startingId, inAzure=0, questions=[q], answer=a, rating=0)
        startingId += 1

        if translatorToEn:
            qnew = translatorToEn.translate([q])[0]
        resp = QuerryAzure(qnew, context = None, source = SOURCE, filters = None)["answers"][0]
        if not addtoDB:
            if resp["answer"] != "No answer found":
                pair = QApair.query.get(resp["id"])
                lq.AzureId = pair.id
                lq.inAzure = 1
                lq.AzureQuestion = translatorToFin.translate(resp["questions"]) if translatorToFin else resp["questions"]
                lq.AzureAnswer = translatorToFin.translate([resp["answer"]])[0] if translatorToFin else resp["answer"]
                if resp["metadata"]["rating"]:
                    lq.AzureRating = int(resp["metadata"]["rating"])

        if ratings is not None:
            lq.rating = ratings[i]

        
        Current.append(lq)
        if addtoDB:
            addQuestions(lq, translatorToEn)
        


# FIX
def addQuestions(locp:localQuestion, transToEn:Translator=None):

    if locp.inAzure > 0:
        #TODO: raise error here
        return 

    questionsToAz = transToEn.translate(locp.questions) if transToEn else locp.questions
    answerToAz = transToEn.translate([locp.answer])[0] if transToEn else locp.answer
    source = SOURCE

    addQuestionsAzure(ids=[locp.id], questions=[questionsToAz], answers=[answerToAz], sources=[source], ratings=[locp.rating])

    newPair = QApair(id=locp.id, answer =locp.answer, source= SOURCE, context="", rating = locp.rating)
    for q in locp.questions:
        newQ = Question(question = q)
        newPair.questions.append(newQ)
        db.session.add(newQ)
    tag = Tag(key="topic", value ="chatgpt") #TODO: stop generic
    db.session.add(tag)
    newPair.tags.append(tag)
    db.session.add(newPair)
    db.session.commit()

    locp.inAzure = 2


# FIX
def UpdateQuestions(ids: List[int], questions: List[str], answers: List[str], sources: List[str], tags: List[List[Tuple[str, str]]], Azure: bool = True, transtoEn:Translator = None):

    for id, q, a, s, t in zip(ids, questions, answers, sources, tags):
        pair = QApair.query.filter_by(id=id).first()
        if q is not None:
            pair.questions = [q]
        if a is not None:
            pair.answer = a
        if s is not None:
            pair.source = s
        if t is not None:
            pair.tags = []
            for t1 in t:
                tag = Tag(key=t1[0], value=t1[1])
                pair.tags.append(tag)

    if Azure:
        UpdateQuestionsAzure(ids, 
                             transtoEn.translate(questions) if transtoEn else questions, 
                             transtoEn.translate([answers])[0] if transtoEn else answers, 
                             sources, tags)


# FIX
def DeleteQuestions(ids: List[int], Azure=True):
    for id in ids:
        QApair.query.filter_by(id=id).delete()
        db.session.commit()

    if Azure:
        DeleteQuestionsAzure(ids)