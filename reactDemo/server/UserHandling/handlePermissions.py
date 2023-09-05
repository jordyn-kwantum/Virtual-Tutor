from flask import Blueprint, jsonify, request
from Database.models import User, db

getListOfStudents = Blueprint("getListOfStudents", __name__)
updateStudentTeam = Blueprint("updateStudentTeam", __name__)
updateIsTeacher = Blueprint("updateIsTeacher", __name__)

@getListOfStudents.route("/api/GetStudents", methods=["GET"])
def get_students_list():
    students = User.query.all()
    data = []
    for student in students:
        team = 1 if student.is_team1 else 2
        teacher = 1 if student.is_teacher else 2
        data.append({
            "id":student.id,
            "email":student.email,
            "team": team,
            "teacher":teacher
        })
    return jsonify({"data":data}), "200"

@updateStudentTeam.route("/api/updateStudentTeam", methods=["POST"])
def update_student_team():
    student_id = request.json["student"]["student_id"]
    team = request.json["student"]["team"]
    team = True if int(team) ==1 else False

    student = User.query.get(student_id)
    student.is_team1 = team
    db.session.commit()
    return "200"


@updateIsTeacher.route("/api/updateIsTeacher", methods=["POST"])
def update_user_role():
    print(request.json)
    student_id = request.json["student"]["student_id"]
    teacher = request.json["student"]["teacher"]
    teacher = True if int(teacher) == 1 else False

    student = User.query.get(student_id)
    print(student.is_teacher)
    student.is_teacher = teacher
    print(student.is_teacher)
    db.session.commit()
    return "200"