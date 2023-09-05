from flask import Flask
from Database.models import db, QApair, Question, Tag, LocalQApair, LocalQuestion
from config import ApplicationConfig
from flask_cors import CORS
from sentence_transformers import SentenceTransformer
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
from QuestionsAndAnswers.currentQuestions import CurrentQuestions
from config import SOURCE


# app is the main server object
app = Flask(__name__)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
# Encryption used for login

# Cookies for sessioning
server_session = Session(app)

# Cross referencing between webpages
cors = CORS(app, resources={ r"/*": { "origins":"*"} }, supports_credentials=True)

# initializiation of the database and session
db.init_app(app)
server_session.init_app(app)

# model used for scoring
model = SentenceTransformer('all-MiniLM-L6-v2')

# create the database
with app.app_context():
    db.create_all()

    # Delete currently existing columns on startup
    Tag.query.delete()
    Question.query.delete()
    QApair.query.delete()
    LocalQuestion.query.delete()
    LocalQApair.query.delete()
    db.session.commit()

    # Fetch questions new from azure.
    DE.addAllQuestions(source = SOURCE)

#Gamestate object that holds where we currenlty are in the game. Starts in state BEFOREGAME
gameState = GameState()
gameState.setGameState(GameStateEnum.BEFOREGAME)

# Creation of the current questions object. Initialized to nothing.
current = CurrentQuestions()
current.ids = []


# Register all of the webpages
# This adds all of the routes to API calls main app.
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

QuestionPage = constructQuestionPagesBlueprint(gameState, current)
app.register_blueprint(QuestionPage)

scorePage = constructScoresPageBlueprint(model, current)
app.register_blueprint(scorePage)



# Start the application
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
