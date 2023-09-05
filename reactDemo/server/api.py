from flask import Flask, jsonify
from Database.models import db, QApair, Question, Tag, User
from config import ApplicationConfig
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_session import Session
from QuestionsAndAnswers.gameState import GameState, constructGameReadyBlueprint, GameStateEnum

import Database.DataEntry as DE

from UserHandling.login import logoutPage, constructLoginBlueprint
from UserHandling.register import constructRegisterBlueprint
from UserHandling.userHomepage import userHomepage
from UserHandling.handlePermissions import getListOfStudents, updateStudentTeam, updateIsTeacher
from Assignments.assignmentPages import constructAssignmentPageBlueprint

from QuestionsAndAnswers.questions import constructQuestionPagesBlueprint
from QuestionsAndAnswers.scores import constructScoresPageBlueprint
from QuestionsAndAnswers.currentQuestions import localQuestion

from typing import List
from config import SOURCE, FINNISH_MODE

from Language.translation import Translator, Language


# app is the main server object
app = Flask(__name__)
app.config.from_object(ApplicationConfig)

# encryption used for login
bcrypt = Bcrypt(app)

# cookies for sessioning
server_session = Session(app)

# cross referencing between webpages
cors = CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})
# cors = CORS(app)

# initializiation of the database and session
db.init_app(app)
server_session.init_app(app)

translatorToFin:Translator = None
translatorToEn:Translator= None

if FINNISH_MODE:
    translatorToFin = Translator(Language.ENGLISH, Language.FINNISH)
    translatorToEn = Translator(Language.FINNISH, Language.ENGLISH)

# create the database
with app.app_context():
    db.create_all()

    # Delete currently existing columns on startup
    Tag.query.delete()
    Question.query.delete()
    QApair.query.delete()
    # User.query.delete()
    # LocalQuestion.query.delete()
    # LocalQApair.query.delete()
    db.session.commit()

    # Fetch questions new from azure.
    DE.addAllQuestions(source = SOURCE, translator = translatorToFin)
    # DE.deleteAllQuestions(source = SOURCE)
    # DE.addKBQuestions("../KB.txt")

#Gamestate object that holds where we currenlty are in the game. Starts in state BEFOREGAME
gameState = GameState()
gameState.setGameState(GameStateEnum.BEFOREGAME)

# Creation of the current questions object. Initialized to nothing.
current:List[localQuestion] = []


# register all of the webpages
# this adds all of the routes to API calls main app
loginPage = constructLoginBlueprint(bcrypt)
app.register_blueprint(loginPage)

app.register_blueprint(logoutPage)

registerPage = constructRegisterBlueprint(bcrypt)
app.register_blueprint(registerPage)

app.register_blueprint(userHomepage)

app.register_blueprint(getListOfStudents)

app.register_blueprint(updateStudentTeam)

app.register_blueprint(updateIsTeacher)

getAssignmentPage = constructAssignmentPageBlueprint(gameState)
app.register_blueprint(getAssignmentPage)

gameReadyPage = constructGameReadyBlueprint(gameState, current)
app.register_blueprint(gameReadyPage)

QuestionPage = constructQuestionPagesBlueprint(gameState, current, translatorToFin, translatorToEn)
app.register_blueprint(QuestionPage)

scorePage = constructScoresPageBlueprint(current, translatorToFin, translatorToEn)
app.register_blueprint(scorePage)



# Start the application
if __name__ == '__main__':
    app.run(debug=False, threaded=True)
