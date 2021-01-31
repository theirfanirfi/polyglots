from flask_classful import FlaskView, route
from flask import request, jsonify
from application import db
from sqlalchemy import text
from application.models.models import Groups, Level, LevelSchema, GroupSchema

class APILevelView(FlaskView):

	def index(self):
		pass

	##get levels
	def get(self, id):
		groups = Groups.query.filter_by(level_id=id).all()
		return jsonify(GroupSchema(many=True).dump(groups))


