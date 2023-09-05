from flask import Blueprint, request, session, jsonify
from Database.models import User


logoutPage = Blueprint("logout_page", __name__)

def constructLoginBlueprint(bcrypt):
    loginPage = Blueprint("login_page", __name__)


    @loginPage.route("/api/login", methods = ["POST"])
    def loginUser():
        email = request.json["email"]
        password = request.json["password"]

        user = User.query.filter_by(email = email).first()

        if user is None:
            return jsonify({
                "error": "Unauthorized"
            }), "401"

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({
                        "error": "Unauthorized"
                    }), "401"


        session["user_id"] = user.id

        return "200"


    return loginPage



@logoutPage.route("/api/logout", methods=["POST"])
def logout_user():
    session.pop("user_id")
    return "200"
