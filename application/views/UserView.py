from flask_classful import FlaskView, route
from application.models.models import *
from flask import render_template, request
from application import db
from flask import redirect, url_for
from application.forms.forms import LoginForm, SignupForm
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user
from application import login_manager

@login_manager.user_loader 
def load_user(user_id):
	return User.query.get(user_id)

class UserView(FlaskView):
	@route('/login',methods=['GET','POST'])
	def login(self):
		form = LoginForm()
		if form.validate_on_submit():
			user = User.query.filter_by(email=form.email.data).first()
			if user:
				if check_password_hash(user.password,form.password.data):
					login_user(user)
					return redirect(url_for('ContinentView:continents'))
				else:
					return "Your password is incorrect"
			else:
				return "This user does not exist"
		else:
			return render_template('login.html',form=form)

	@route('/signup',methods=['GET','POST'])
	def signup(self):
		form = SignupForm()
		if form.validate_on_submit():
			hashed_password = generate_password_hash(form.password.data,method='sha256')
			new_user = User(email=form.email.data,
				password=hashed_password)
			try:
				db.session.add(new_user)
				db.session.commit()
				return redirect(url_for('UserView:login'))
			except:
				return "There was an issue"

		return render_template('signup.html',form=form)

	@route("/logout")
	@login_required
	def logout(self):
		logout_user()
		return redirect(url_for('UserView:login'))