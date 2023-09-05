from flask_sqlalchemy import SQLAlchemy 
from uuid import uuid4

"""
This file defines the local database tables.
"""

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex 

class User(db.Model): # type:ignore
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key = True, unique=True, default = get_uuid)
    email = db.Column(db.String(345), unique = True)
    password = db.Column(db.Text, nullable=False)
    is_teacher = db.Column(db.Boolean, default = False)
    is_team1 = db.Column(db.Boolean, default = True)

class Question(db.Model): #type:ignore
    __tablename__ = "questiontable"

    id = db.Column("id", db.Integer, primary_key = True)
    question = db.Column("question", db.String(300), nullable = False)
    QApairid = db.Column(db.Integer, db.ForeignKey("qapairtable.id"), nullable=False)

class Tag(db.Model): #type:ignore
    __tablename__ = "tagstable"
    id = db.Column("id", db.Integer, primary_key=True)
    key = db.Column("key", db.String(50), nullable=False)
    value = db.Column("value", db.String(50), nullable=False)
    QApairid = db.Column(db.Integer, db.ForeignKey("qapairtable.id"), nullable=False)

class QApair(db.Model): #type: ignore
    __tablename__ = "qapairtable"
    
    id = db.Column(db.Integer, primary_key = True)
    questions = db.relationship("Question", backref="qapair", lazy=True, cascade="all,delete, delete-orphan")
    answer = db.Column(db.String(300), nullable = False)
    tags = db.relationship("Tag", backref="qapair", lazy=True, cascade="all,delete, delete-orphan")
    source = db.Column(db.String(300), nullable = False)
    context = db.Column(db.String(500))
    rating = db.Column(db.Integer, default = 0)


# class LocalQuestion(db.Model): #type:ignore
#     __tablename__ = "localquestiontable"

#     id = db.Column("id", db.Integer, primary_key = True)
#     question = db.Column("question", db.String(300), nullable = False)
#     LocalQApair = db.Column(db.Integer, db.ForeignKey("localqapairtable.id"), nullable=False)

# class Team2Question(db.Model): #type:ignore
#     __tablename__ = "team2questiontable"

#     id = db.Column("id", db.Integer, primary_key = True)
#     question = db.Column("question", db.String(300), nullable = False)
#     LocalQApair = db.Column(db.Integer, db.ForeignKey("localqapairtable.id"), nullable=False)

# class LocalQApair(db.Model): #type: ignore
#     __tablename__ = "localqapairtable"

#     id = db.Column(db.Integer, primary_key = True)
#     questions = db.relationship("LocalQuestion", backref="localqapair", lazy=True, cascade="all, delete, delete-orphan")
#     answer = db.Column(db.String(300), nullable = False)
#     AzureId = db.Column(db.Integer, db.ForeignKey("qapairtable.id"))
#     AzurePair = db.relationship("QApair", foreign_keys = AzureId)
#     rating = db.Column(db.Integer, default = 0)
#     Team2Question = db.relationship("Team2Question", backref="localqapair", lazy=True, cascade="all, delete, delete-orphan")
#     Flag = db.Column(db.Boolean, default = False)
#     IsSelected = db.Column(db.Boolean, default=False)