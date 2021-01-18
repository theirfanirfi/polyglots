from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/polygolt"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "UserView:login"


from application.models.models import *
from application.views.ContinentView import ContinentView
from application.views.CountryView import CountryView
from application.views.LanguageView import LanguageView
from application.views.LevelView import LevelView
from application.views.GroupView import GroupView
from application.views.LessonView import LessonView
from application.views.UserView import UserView
from application.views.WordView import WordView

ContinentView.register(app, route_base="/admin/continents")
CountryView.register(app, route_base="/admin/countries")
LanguageView.register(app, route_base="/admin/languages")
LevelView.register(app, route_base="/admin/levels")
GroupView.register(app, route_base="/admin/groups")
LessonView.register(app, route_base="/admin/lessons")
UserView.register(app, route_base="/admin/users")
WordView.register(app, route_base="/admin/words")