from flask import Blueprint, session, jsonify
from Database.models import User

userHomepage = Blueprint("user_homepage", __name__)

@userHomepage.route("/api/@me")
def getUserHomePage():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({
            "error": "Unauthorized"
        }), "401"

    user = User.query.filter_by(id = user_id).first()
    team = 1 if user.is_team1 else 2
    return jsonify({
        "id":user.id,
        "email":user.email,
        "teacher":user.is_teacher,
        "team": team
    }), "200"