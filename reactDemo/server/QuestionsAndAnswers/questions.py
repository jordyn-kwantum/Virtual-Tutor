from flask import Blueprint, request, jsonify, session
import Database.DataEntry as DE
from typing import List, Tuple
from Database.models import QApair, db, User, Question
from QuestionsAndAnswers.gameState import GameState
from QuestionsAndAnswers.currentQuestions import localQuestion
from AzureCommunication.UpdateAzureDatabase import UpdateQuestionsAzure, QuerryAzure
import random
from config import SOURCE
from typing import List
from Language.translation import Translator

def constructQuestionPagesBlueprint(gameState:GameState, current:List[localQuestion], translatorToFin:Translator=None, translatorToEn:Translator=None):
    QuestionsPages = Blueprint("addQuestionsPage", __name__)


    @QuestionsPages.route("/api/AddQuestions", methods=["POST"])
    def add_questions():
        questions = []
        answers = []
        for elem in request.json["QApairs"]:
            questions.append(elem["question"])
            answers.append(elem["answer"])

        
        DE.addLocalQuestions(questions, answers, current,translatorToEn=translatorToEn, translatorToFin=translatorToFin)

        return "200"


    @QuestionsPages.route("/api/deleteCurrentQuestion", methods=["POST"])
    def delete_local_question():
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({
                "error": "Unauthorized"
            }), "401"
        user = User.query.filter_by(id = user_id).first()
        if not user.is_teacher:
            return jsonify({
                    "error": "Unauthorized"
                }), "401"

        targetId = int(request.json["id"])
        currentId = -1
        for i, pair in enumerate(current):
            if pair.id == targetId:
                currentId = i
                break
        if currentId >= 0:
            del current[currentId]

        return "200"

    @QuestionsPages.route("/api/rejectCurrentQuestion", methods=["POST"])
    def reject_selected_question():
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({
                "error": "Unauthorized"
            }), "401"
        user = User.query.filter_by(id = user_id).first()
        if not user.is_teacher:
            return jsonify({
                    "error": "Unauthorized"
                }), "401"

        targetId = int(request.json["id"])
        for pair in current:
            if pair.id == targetId:
                pair.selected = False
                break

        return "200"


    @QuestionsPages.route("/api/AddQuestionsTeacher", methods = ["POST"])
    def add_questions_teacher():
        questions = []
        answers = []
        ratings = []
        for elem in request.json["QApairs"]:
            questions.append(elem["question"])
            answers.append(elem["answer"])
            ratings.append(int(elem["rating"]))

        
        DE.addLocalQuestions(questions, answers, current, ratings, addtoDB=True,translatorToEn=translatorToEn, translatorToFin=translatorToFin)

        return "200"


    @QuestionsPages.route("/api/AddLocalQuestionToDB", methods=['POST'])
    def add_local_question_to_db():
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({
                "error": "Unauthorized"
            }), "401"
        user = User.query.filter_by(id = user_id).first()
        if not user.is_teacher:
            return jsonify({
                    "error": "Unauthorized"
                }), "401"
        
        targetId = int(request.json["id"])
        for pair in current:
            if targetId == pair.id:
                DE.addQuestions(pair, translatorToEn)
        pair.inAzure = 2
        return "200"

    @QuestionsPages.route("/api/preferDatabaseFormulation", methods=['POST'])
    def prefer_DB_Formulation():
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({
                "error": "Unauthorized"
            }), "401"
        user = User.query.filter_by(id = user_id).first()
        if not user.is_teacher:
            return jsonify({
                    "error": "Unauthorized"
                }), "401"
        
        targetid = int(request.json["id"])
        for pair in current:
            if pair.id == targetid:
                lq = pair
                break
        
        assert lq.inAzure == 1, "added question does not have an azure counterpart"
        
        lq.questions = []
        for q in lq.AzureQuestion:
            lq.questions.append(q)
        lq.answer = lq.AzureAnswer
        lq.inAzure = 2
        lq.rating = lq.AzureRating
        return "200"


    @QuestionsPages.route("/api/mergeLocalDBquestionToGlobal", methods=['POST'])
    def mergeLocalDBquestionToGlobal():
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({
                "error": "Unauthorized"
            }), "401"
        user = User.query.filter_by(id = user_id).first()
        if not user.is_teacher:
            return jsonify({
                    "error": "Unauthorized"
                }), "401"
        
        targetId = int(request.json["id"])
        for pair in current:
            if pair.id == targetId:
                lq = pair
                break

        assert lq.inAzure == 1, "local question does not have azure counterpart"

        # pair = LocalQApair.query.get(int(request.json["id"]))
        globalPair = QApair.query.get(lq.AzureId)
        # gpair = pair.AzurePair
        qs = lq.questions
        questions = []
        for q in qs:
            newQ = Question(question = q)
            questions.append([q])
            db.session.add(newQ)
            globalPair.questions.append(newQ)
        db.session.commit()
        lq.inAzure = 2

        UpdateQuestionsAzure([globalPair.id], questions=questions)
        return "200"
    

    @QuestionsPages.route("/api/addGlobalQuestionToCurrent", methods=['POST'])
    def addGlobalQuestionToCurrent():
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({
                "error": "Unauthorized"
            }), "401"
        user = User.query.filter_by(id = user_id).first()
        if not user.is_teacher:
            return jsonify({
                    "error": "Unauthorized"
                }), "401"
        
        pair = QApair.query.get(int(request.json["id"]))

        lq = localQuestion(id = pair.id, inAzure=2, questions=[], answer=pair.answer, source=pair.source, 
                            context=pair.context, rating=pair.rating, AzureId = pair.id, AzureQuestion = [], 
                            AzureAnswer=pair.answer, AzureRating=pair.rating, selected=True)

        qs = pair.questions
        for q in qs:
            lq.questions.append(q.question)
            lq.AzureQuestion.append(q.question)
        
        current.append(lq)

        return "200"
        

    @QuestionsPages.route("/api/GetQAPairs", methods=["GET"])
    def get_current_qa_pairs():
        user_id = session.get("user_id")
        if not user_id:
                return jsonify({
                    "error": "Unauthorized"
                }), "401"
        user = User.query.filter_by(id = user_id).first()
        if not user.is_teacher:
            return jsonify({
                    "error": "Unauthorized"
                }), "401"
        
        data = { 
            "local":[],
            "global":[]
        }
        # print(current.ids)
        for i, lq in enumerate(current):
            # qapair = LocalQApair.query.get(id)
            data["local"].append({
                "id":lq.id,
                "questions":lq.questions,
                "answer":lq.answer,
                "rating":lq.rating,
                "flag": True if lq.inAzure <=1 else False,
                "selected":lq.selected
            })  
            if lq.inAzure > 0:
                data["local"][i]["A_questions"] = lq.AzureQuestion
                data["local"][i]["A_Answer"] = lq.AzureAnswer

        globalPairs = QApair.query.all()
        for pair in globalPairs:
            questions = []
            tags = []
            for q in pair.questions:
                questions.append(q.question)
            for tag in pair.tags:
                tags.append({
                    tag.key:tag.value
                })
            data["global"].append({
                "id":pair.id,
                "questions":questions,
                "answer":pair.answer,
                "rating":pair.rating,
                "tags":tags,
                "source":pair.source,
                "contex":pair.context
            })
        return jsonify({"pairs":data})


    @QuestionsPages.route("/api/GetQAPairsStudent", methods = ["GET"])
    def get_current_qa_pairs_student():
        user_id = session.get("user_id")
        if not user_id:
                return jsonify({
                    "error": "Unauthorized"
                }), "401"
        user = User.query.filter_by(id = user_id).first()
        if not user.is_team1:
            return jsonify({
                    "error": "Unauthorized"
                }), "401"
        data = []
        for lq in current:
            data.append({
                "id":lq.id,
                "question":lq.questions,
                "answer":lq.answer,
                "selected":lq.selected
            })  
        return jsonify(data), "200"

    @QuestionsPages.route("/api/StudentSubmitQuestions", methods=["POST"])
    def SetTeam1QuestionList():
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({
                "error": "Unauthorized"
            }), "401"
        user = User.query.filter_by(id = user_id).first()
        if not (user.is_team1 or user.is_teacher):
            return jsonify({
                    "error": "Unauthorized"
                }), "401"
        
        ids = request.json["ids"]
        if len(ids) >= 6:
            return jsonify({
                "error":"Too many elements in List",
            }), "406"

        for pair in current:
            if pair.id in ids:
                pair.selected = True

        return "200"
            


    @QuestionsPages.route("/api/GetAnswers", methods=["GET"])
    def get_current_local_answers():
        user_id = session.get("user_id")
        if not user_id:
                return jsonify({
                    "error": "Unauthorized"
                }), "401"
        data = []
        for lq in current:
            data.append({
                "id":lq.id,
                "answer":lq.answer,
            })
        return jsonify({"pairs":data})


    @QuestionsPages.route("/api/updateQuestionRating", methods=["POST"])
    def update_rating():
        user_id = session.get("user_id")
        if not user_id:
                return jsonify({
                    "error": "Unauthorized"
                }), "401"
        user = User.query.filter_by(id = user_id).first()
        if user.is_teacher:
            v = request.json["question"]
            id = v["id"]
            rating = int(v["rating"])

            if rating < 0 or rating > 3:
                return "401"
            c = QApair.query.get(id)
            c.rating = rating
            db.session.commit()
            return "200"


    @QuestionsPages.route("/api/updateLocalQuestionRating", methods=["POST"])
    def update_local_rating():
        user_id = session.get("user_id")
        if not user_id:
                return jsonify({
                    "error": "Unauthorized"
                }), "401"
        user = User.query.filter_by(id = user_id).first()
        if user.is_teacher:
            v = request.json["question"]
            targetid = int(v["id"])
            rating = int(v["rating"])

            if rating < 0 or rating > 3:
                return "401"
            
            for pair in current:
                if pair.id == targetid:
                    lq = pair
                    break

            lq.rating = rating
            return "200"

    

    @QuestionsPages.route("/api/checkQuestions", methods=["POST"])
    def check_team2_questions():
        user_id = session.get("user_id")
        if not user_id:
                return jsonify({
                    "error": "Unauthorized"
                }), "401"
        for elem in request.json["questions"]:
            targetid = int(elem["id"])

            question = elem["question"]

            for pair in current:
                if pair.id == targetid:
                    lq = pair
                    break

            # localQa = LocalQApair.query.get(id)
            # newq = Team2Question(question = question)
            lq.team2question = question
            # db.session.add(newq)
        # db.session.commit()
        return "200"

    return QuestionsPages