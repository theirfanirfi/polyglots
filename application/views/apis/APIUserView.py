from flask_classful import FlaskView, route
from application.models.models import *
from flask import request
from application import db
from flask import redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from application import login_manager
import random
from application.utils import send_email
from application.views.apis.utils import (
    AuthorizeRequest,
    notLoggedIn,
    getPasswordResetUser,
    getPasswordResetUserWithoutCode,
)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class APIUserView(FlaskView):
    @route("/login", methods=["POST"])
    def login(self):
        form = request.form
        for field in form:
            if form[field] == "" or form[field] == None:
                return jsonify(
                    {"isLoggedIn": False, "message": "All fields are required"}
                )

        user = User.query.filter_by(email=form["email"]).first()
        if user:
            if check_password_hash(user.password, form["password"]):
                user.token = generate_password_hash(
                    form["password"] + user.fullname, method="sha256"
                )
                try:
                    db.session.add(user)
                    db.session.commit()
                    return jsonify(
                        {
                            "isLoggedIn": True,
                            "message": "Login successful",
                            "user": UserSchema(many=False).dump(user),
                        }
                    )
                except Exception as e:
                    print(e)
                    return jsonify(
                        {"isLoggedIn": False, "message": "Incorrect credentials"}
                    )
            else:
                return jsonify(
                    {"isLoggedIn": False, "message": "Incorrect credentials"}
                )
        else:
            return jsonify({"isLoggedIn": False, "message": "Incorrect credentials"})

    @route("/signup", methods=["POST"])
    def signup(self):
        form = request.form
        for field in form:
            if form[field] == "" or form[field] == None:
                return jsonify(
                    {"isRegistered": False, "message": "All fields are required"}
                )

        checkUser = User.query.filter_by(email=form["email"]).count()
        if checkUser > 0:
            return jsonify(
                {"isRegistered": False, "message": "The email is already taken."}
            )

        confirmation_code = random.randint(1000, 9999)
        hashed_password = generate_password_hash(form["password"], method="sha256")
        token = generate_password_hash(
            form["password"] + form["fullname"], method="sha256"
        )
        new_user = User(
            fullname=form["fullname"],
            email=form["email"],
            age=form["age"],
            gender=form["gender"],
            country=form["country"],
            continent=form["continent"],
            password=hashed_password,
            token=token,
            confirmation_code=confirmation_code,
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            send_email(
                new_user.email,
                "<h1> Confirmation code is: " + str(confirmation_code) + "</h1>",
            )
            return jsonify(
                {
                    "isRegistered": True,
                    "message": "Regsiteration successful, A confirmation code is sent to your email",
                    "user": UserSchema(many=False).dump(new_user),
                }
            )
        except Exception as e:
            print(e)
            return jsonify({"isRegistered": False, "message": str(e)})

    @route("/confirm", methods=["POST"])
    def confirm_account(self):
        print(request.headers)
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(
                {"isConfirmed": False, "message": "Invalid details provided"}
            )

        code = request.form["code"]
        if int(code) == user.confirmation_code:
            user.is_confirmed = 1
            try:
                db.session.add(user)
                db.session.commit()
                return jsonify(
                    {
                        "isConfirmed": True,
                        "message": "Account confirmed",
                        "user": UserSchema(many=False).dump(user),
                    }
                )
            except Exception as e:
                return jsonify(
                    {
                        "isConfirmed": False,
                        "message": "Error occurred, Please try again.",
                    }
                )

        else:
            print("not matched")
            return jsonify(
                {"isConfirmed": False, "message": "Invalid details provided"}
            )

    @route("/send_confirmation_code")
    def send_confirmation_code(self):
        print(request.headers)
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify({"isSent": False, "message": "Invalid details provided"})

        confirmation_code = random.randint(1000, 9999)
        user.confirmation_code = confirmation_code
        try:
            db.session.add(user)
            db.session.commit()
            send_email(
                user,
                "<h1>Your new confirmation code is: "
                + str(confirmation_code)
                + "</h1>",
            )
            return jsonify({"isSent": True, "message": "Confirmation code sent."})
        except Exception as e:
            return jsonify(
                {
                    "isSent": False,
                    "message": "Error occurred in sending the confirmation code. Please try again.",
                }
            )

    @route("/send_password_reset_code", methods=["POST"])
    def send_password_reset_code(self):
        email = request.form["email"]
        user = User.query.filter_by(email=email)
        if user.count() > 0:
            reset_code = random.randint(1000, 9999)
            user = user.first()
            user.reset_code = reset_code
            user.reset_token = generate_password_hash(
                user.email + user.fullname, method="sha256"
            )
            try:
                db.session.add(user)
                db.session.commit()
                send_email(
                    user,
                    "<h1>Your Password reset code is: " + str(reset_code) + "</h1>",
                )
                return jsonify(
                    {
                        "isSent": True,
                        "message": "Password reset code sent to your email",
                        "reset_token": user.reset_token,
                    }
                )
            except Exception as e:
                return jsonify(
                    {
                        "isSent": True,
                        "message": "Password reset code sent to your email",
                        "reset_token": "reset_token",
                    }
                )
        else:
            return jsonify(
                {
                    "isSent": True,
                    "message": "Password reset code sent to your email",
                    "reset_token": "reset_token",
                }
            )

    @route("/confirm_reset_code", methods=["POST"])
    def confirm_reset_code(self):
        form = request.form
        code = form["code"]
        email = form["email"]

        user = getPasswordResetUser(request.headers, email, code)
        if not user:
            return jsonify(
                {
                    "isConfirmed": False,
                    "message": "Invalid details provided.",
                }
            )

        user.reset_token = generate_password_hash(user.token, method="sha256")
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify(
                {
                    "isConfirmed": True,
                    "message": "Account confirmed",
                    "reset_token": user.reset_token,
                }
            )
        except Exception as e:
            return jsonify(
                {
                    "isConfirmed": False,
                    "message": "Error occurred, Please try again.",
                }
            )

    @route("/reset_password", methods=["POST"])
    def reset_password(self):
        form = request.form
        email = form["email"]
        password = form["password"]

        user = getPasswordResetUserWithoutCode(request.headers, email)
        if not user:
            return jsonify(
                {
                    "isReset": False,
                    "message": "Invalid details provided.",
                }
            )

        user.password = generate_password_hash(password, method="sha256")
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify(
                {
                    "isReset": True,
                    "message": "Password reseted, you can login now.",
                }
            )
        except Exception as e:
            return jsonify(
                {
                    "isReset": False,
                    "message": "Error occurred, Please try again.",
                }
            )

    @route("/countries")
    def countries(self):
        countries = Countries.query.all()
        return jsonify(CountriesSchema(many=True).dump(countries))

    @route("/continents")
    def continents(self):
        continents = Continents.query.all()
        return jsonify(ContinentSchema(many=True).dump(continents))

    @route("/registeration_details")
    def registeration_details(self):
        continents = Continents.query.all()
        countries = Countries.query.all()
        data = {
            "countries": CountriesSchema(many=True).dump(countries),
            "continents": ContinentSchema(many=True).dump(continents),
        }
        return jsonify(data)
