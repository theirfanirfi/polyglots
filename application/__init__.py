from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)

app = Flask(__name__)
ma = Marshmallow(app)
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
from application.views.AdsView import AdsView

##apis import
from application.views.apis.LessonView import APILessonView
from application.views.apis.APILanguageView import APILanguageView
from application.views.apis.APILevelView import APILevelView
from application.views.apis.APIUserView import APIUserView
from application.views.apis.APIAcomplishments import APIAcomplishmentsView

ContinentView.register(app, route_base="/admin/continents")
CountryView.register(app, route_base="/admin/countries")
LanguageView.register(app, route_base="/admin/languages")
LevelView.register(app, route_base="/admin/levels")
GroupView.register(app, route_base="/admin/groups")
LessonView.register(app, route_base="/admin/lessons")
UserView.register(app, route_base="/admin/users")
WordView.register(app, route_base="/admin/words")
AdsView.register(app, route_base="/admin/ads")

####### apis
APILessonView.register(app, route_base="/api/lessons")
APILanguageView.register(app, route_base="/api/languages")
APILevelView.register(app, route_base="/api/levels/")
APIUserView.register(app, route_base="/api/users/")
APIAcomplishmentsView.register(app, route_base="/api/acomplishments/")