from flask import Blueprint, session, request, jsonify
from enum import Enum
from Database.models import User, db
from QuestionsAndAnswers.currentQuestions import localQuestion
from typing import List

"""
This class is responsible for the handling of the gamestate. The various states of the game are given below.
"""


class GameStateEnum(Enum):
    BEFOREGAME = 0
    STUDENT1TURN = 1
    TEACHERTURN = 2
    STUDENT1TURNAGAIN = 3
    STUDENT2TURN = 4
    GAMEEND = 5

class GameState():
    
    __GAMEREADY = GameStateEnum.BEFOREGAME

    def getGameStatus(self) -> GameStateEnum:
        return self.__GAMEREADY

    def toggleGameStatus(self):
        self.__GAMEREADY = not self.__GAMEREADY

    def setGameState(self, state:GameStateEnum):
        if not isinstance(state, GameStateEnum):
            raise Exception("game state is not a valid Game State")
        self.__GAMEREADY = state


def constructGameReadyBlueprint(gameState:GameState, current:List[localQuestion]):

    gameStatePage = Blueprint("GameStatePage", __name__)

    @gameStatePage.route("/api/GetGameState", methods=["GET"])
    def get_game_state():
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({
                "error": "Unauthorized"
            }), "401"
        # user = User.query.filter_by(id = user_id).first()
        # if not user.is_teacher:
        #     return jsonify({
        #         "error": "Unauthorized"
        #     }), "401"

        return jsonify({
            "GameState":gameState.getGameStatus().value
        }), "200"


    @gameStatePage.route("/api/startGame", methods=["POST"])
    def startGame():
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

        current = []
        gameState.setGameState(GameStateEnum.STUDENT1TURN)
        return "200"
        

    @gameStatePage.route("/api/Team1TurnEnd", methods=["POST"])
    def Team1TurnEnd():
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

        gameState.setGameState(GameStateEnum.TEACHERTURN)
        return "200"

    @gameStatePage.route("/api/Team1TurnAgain", methods=["POST"])
    def Team1TurnAgain():
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

        gameState.setGameState(GameStateEnum.STUDENT1TURNAGAIN)
        return "200"

    @gameStatePage.route("/api/TeacherTurnEnd", methods=["POST"])
    def TeacherTurnEnd():
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

        # toRemove = []
        # for pair in current:
        #     if not pair.inAzure:
        #         toRemove.append(pair)
        # for pair in toRemove:
        #     current.remove(pair)

        gameState.setGameState(GameStateEnum.STUDENT2TURN)
        return "200"

        

    @gameStatePage.route("/api/Team2TurnEnd", methods=["POST"])
    def Team2TurnEnd():
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
        gameState.setGameState(GameStateEnum.GAMEEND)

        return "200"

    return gameStatePage