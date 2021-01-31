from flask_classful import FlaskView, route
from flask import request, jsonify
from application import db
from sqlalchemy import text
from application.models.models import Language, LanguageSchema, Level, LevelSchema

class APILanguageView(FlaskView):

	def index(self):
		languages = Language.query
		ls = LanguageSchema(many=True)
		languages = ls.dump(languages.all())
		return jsonify(languages)

	##get levels
	def get(self, id):
		levels = Level.query.filter_by(language_id=id).all()
		return jsonify(LevelSchema(many=True).dump(levels))


