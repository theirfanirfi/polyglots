from flask_classful import FlaskView, route
from application.models.models import *
from flask import request
from application import db
from flask import redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from application import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class APIUserView(FlaskView):
    @route('/login', methods=['POST'])
    def login(self):
        form = request.form
        for field in form:
            if form[field] == "" or form[field] == None:
                return jsonify({'isLoggedIn': False, 'message': 'All fields are required'})

        user = User.query.filter_by(email=form['email']).first()
        if user:
            if check_password_hash(user.password, form['password']):
                user.token = generate_password_hash(form['password']+user.fullname, method='sha256')
                try:
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({'isLoggedIn': True,
                                    'message': 'Login successful',
                                    'user': UserSchema(many=False).dump(user)})
                except Exception as e:
                    print(e)
                    return jsonify({'isLoggedIn': False, 'message': 'Incorrect credentials'})
            else:
                return jsonify({'isLoggedIn': False, 'message': 'Incorrect credentials'})
        else:
            return jsonify({'isLoggedIn': False, 'message': 'Incorrect credentials'})

    @route('/signup', methods=['POST'])
    def signup(self):
        form = request.form
        for field in form:
            if form[field] == "" or form[field] == None:
                return jsonify({'isRegistered': False, 'message': 'All fields are required'})


        checkUser = User.query.filter_by(email=form['email']).count()
        if checkUser > 0:
            return jsonify({'isRegistered': False, 'message': 'The email is already taken.'})

        hashed_password = generate_password_hash(form['password'], method='sha256')
        token = generate_password_hash(form['password']+form['fullname'], method='sha256')
        new_user = User(fullname=form['fullname'], email=form['email'], age=form['age'],
                        gender=form['gender'], country_id=form['country'],
                        continent_id=form['continent'], password=hashed_password,
                        token=token)
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'isRegistered': True, 'message': 'Regsiteration successful', 'user': UserSchema(many=False).dump(new_user)})
        except Exception as e:
            print(e)
            return jsonify({'isRegistered': False, 'message': str(e)})

    @route('/countries')
    def countries(self):
        countries = Countries.query.all()
        return jsonify(CountriesSchema(many=True).dump(countries))

    @route('/continents')
    def continents(self):
        continents = Continents.query.all()
        return jsonify(ContinentSchema(many=True).dump(continents))

    @route('/registeration_details')
    def registeration_details(self):
        continents = Continents.query.all()
        countries = Countries.query.all()
        data = {
            'countries': CountriesSchema(many=True).dump(countries),
            'continents': ContinentSchema(many=True).dump(continents)
        }
        return jsonify(data)
