from flask_classful import FlaskView, route
from flask import request, jsonify
from application import db
from sqlalchemy import text
from application.models.models import (
    Language,
    LanguageSchema,
    Level,
    LevelSchema,
    GroupSchema,
)
from application.views.apis.utils import AuthorizeRequest, notLoggedIn
from application.utils import send_email


class APILanguageView(FlaskView):
    def index(self):
        languages = Language.query
        ls = LanguageSchema(many=True)
        languages = ls.dump(languages.all())
        return jsonify(languages)

    ##get levels
    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        levels_list = list()
        levels = db.engine.execute(
            text(
                "SELECT *, (select count(*) from groups where level_id=level.level_id) as total_groups,"
                + "(select count(*) from accomplishments WHERE level_id = level.level_id AND language_id = level.language_id AND user_id = "
                + str(user.user_id)
                + ") as total_done"
                + " FROM level WHERE level.language_id = "
                + str(id)
            )
        )
        groupSchema = GroupSchema()
        groupSchema.many = True
        for level in levels:
            data = {}
            data["level"] = LevelSchema(many=False).dump(level)
            groups_sql = text(
                "SELECT *, (select count(*) from lessons where lessons.group_id=groups.group_id) as total_lessons"
                + " FROM groups WHERE level_id = "
                + str(level.level_id)
                + " AND groups.language_id="
                + str(level.language_id)
            )
            groups = db.engine.execute(groups_sql)
            data["groups"] = groupSchema.dump(groups)
            levels_list.append(data)

        return jsonify(levels_list)
