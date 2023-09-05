from flask import Blueprint, request, session, jsonify
from Database.models import User, db

def constructRegisterBlueprint(bcrypt):

    registerPage = Blueprint("register_page", __name__)

    @registerPage.route("/api/register", methods =["POST"])
    def register_user():
        email = request.json["email"]
        password = request.json["password"]
        is_teacher = str(request.json["is_teacher"]).lower() == "true"

        try:

            user_exists = User.query.filter_by(email = email).first() is not None  

            if user_exists:
                return jsonify({
                    "error": "User already exists"
                }), "409"
            hashed_password = bcrypt.generate_password_hash(password)
            new_user = User(email=email, password = hashed_password, is_teacher = is_teacher)
            print(new_user)

            db.session.add(new_user)
            db.session.commit()

            session["user_id"] = new_user.id
            
        except Exception as e:
            return  jsonify({"error":e}), "200"
        
        return "200"

    @registerPage.route("/api/massRegister", methods=["POST"])
    def massregister():
        user_id = session.get("user_id")
        if not user_id:
            return jsonify({
                "error": "Unauthorized"
            }), "401"
        user = User.query.filter_by(id = user_id).first()
        if not user.is_teacher:
            return jsonify({
                "error":"Unauthorized"
            }), "401"

        students = request.json["Students"]
        for student in students:
            name = student["name"]
            email = student["email"]
            password = student["password"]

            hashed_password = bcrypt.generate_password_hash(password)
            new_user = User(email=email, password = hashed_password, is_teacher = False)
            db.session.add(new_user)
        db.session.commit()
        return "200"

    @registerPage.route("/api/deleteAccount",  methods = ["POST"])
    def deleteAccount():
        email = request.json["student_email"]
        User.query.filter_by(email = email).delete()
        db.session.commit()
        return "200"

    return registerPage