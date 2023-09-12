from flask import Blueprint, jsonify
from QuestionsAndAnswers.gameState import GameState
from Language.translation import Translator, Language
from typing import List
import os
from config import FINNISH_MODE



# This file loads the hardcoded assignment into the web UI
def get_assignment_text() -> List[str]:
    filename = "ChatGPTfi.txt" if FINNISH_MODE else "ChatGPT.txt"
    with open(os.path.join("Assignments", filename), 'r', encoding='utf-8') as fp:
        text = []
        for line in fp.readlines():
            line = str(line)    
            line = line.strip()
            line = line.replace("\r\n", "")
            text.append(line)
    # langs = Translator.detectLanguage(text)
    # if TRANSLATE and langs[0] != "en":
    #     if langs[0] == "nl":
    #         startLanguage = Language.DUTCH
    #     if langs[0] == "fi":
    #         startLanguage = Language.FINNISH
    #     tran = Translator(startLanguage, Language.ENGLISH)
    #     text = tran.translate(text)
    return text     


# Constructor for creating the flask blueprint, that allows the assignment page to be called
def constructAssignmentPageBlueprint(gameState:GameState):
    getAssignmentPage = Blueprint("get_assignment_page", __name__)

    # Route for the assignment page. Returns a JSON object with the required data
    @getAssignmentPage.route("/api/GetAssignment", methods=["GET"])
    def get_assignment():
        title = "Analyysi: Melkein jokaisen on totuttava chatbottien keskusteluun" if FINNISH_MODE else "Analysis: Almost everyone needs to get used to chatbots chattering"
        paragraphs = get_assignment_text()
        data = {
            "title":title,
            "text": [],
        }
        for para in paragraphs:
            data["text"].append(para)
        return jsonify(data), '200'

    return getAssignmentPage