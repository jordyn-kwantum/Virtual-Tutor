from flask import Blueprint, jsonify, request, session
from Database.models import QApair, db
import Database.DataEntry as DE
from QuestionsAndAnswers.currentQuestions import localQuestion
from AzureCommunication.UpdateAzureDatabase import QuerryAzure
from config import SOURCE
from typing import List
from Language.translation import Translator

def constructScoresPageBlueprint(current:List[localQuestion], translatorToFin:Translator = None, translatorToEn:Translator = None):

    scoresPage = Blueprint("scoresPage", __name__)

    @scoresPage.route("/api/getScores", methods=["GET"])
    def get_scores():
        data = []
        user_id = session.get("user_id")
        if not user_id:
                return jsonify({
                    "error": "Unauthorized"
                }), "401"
        for pair in current:
            # localQA = LocalQApair.query.get(id)
            question = pair.team2question
            
            score = 0 
            maxscore = pair.rating

            resp = QuerryAzure(
                 translatorToEn(question) if translatorToEn else question, 
                 context=None, source = SOURCE, filters=None)
            resp = resp["answers"]
            for answ in resp:
                if answ["id"] == pair.id:
                    score = answ["confidenceScore"] * maxscore
                    break
            
            data.append({
                "score":score,
                "maxscore":maxscore,
                "TrueQuestion":pair.questions[0],
                "GivenQuestion":pair.team2question,
                "Answer":pair.answer,
            })

        return jsonify({"scores":data}), "200"

    return scoresPage