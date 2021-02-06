from flask_classful import FlaskView, route
from flask import request, jsonify
from application import db
from sqlalchemy import text, and_
from application.models.models import (
    Lessons,
    LessonSchema,
    Questionnaire,
    QuestionnaireSchema,
    Advertisements,
    AdSchema,
)
from application.builders.LessonBuilder import SimpleSentenceLessonBuilder
from application.views.apis.utils import AuthorizeRequest, notLoggedIn


class APILessonView(FlaskView):
    def index(self):
        lessons = list()
        ls = LessonSchema()
        sentences = Lessons.query.filter_by()
        if sentences.count() > 0:
            sentences = sentences.all()
            for s in sentences:
                if s.is_straight_translation == 1 or s.is_multiple_images:
                    lesson = (
                        SimpleSentenceLessonBuilder(s)
                        .split_into_words()
                        .create_dropDown()
                        .build()
                    )
                    lessons.append(lesson)
                else:
                    data = {}
                    data["lesson"] = ls.dump(s)
                    data["dropdown"] = {}
                    lessons.append(data)

        return jsonify(lessons)

    @route("/group/<int:group_id>")
    def group_lessons(self, group_id):
        user = AuthorizeRequest(request.headers)
        print(user)
        if not user:
            return jsonify(notLoggedIn)

        lessons = list()
        ls = LessonSchema()
        sentences = Lessons.query.filter_by(group_id=group_id)
        questionnaire = Questionnaire.query.filter_by(group_id=group_id).first()
        ads = Advertisements.query.filter(
            user.age >= Advertisements.ad_age,
            Advertisements.ad_gender == user.gender,
            Advertisements.is_bottom_ad == 0,
        ).all()
        bottom_ads = Advertisements.query.filter(
            user.age >= Advertisements.ad_age,
            Advertisements.ad_gender == user.gender,
            Advertisements.is_bottom_ad == 1,
        ).all()
        if sentences.count() > 0:
            sentences = sentences.all()
            for s in sentences:
                if s.is_straight_translation == 1 or s.is_multiple_images:
                    lesson = (
                        SimpleSentenceLessonBuilder(s)
                        .split_into_words()
                        .create_dropDown()
                        .build()
                    )
                    lessons.append(lesson)
                else:
                    data={}
                    data["lesson"] = ls.dump(s)
                    data["dropdown"] = {}
                    lessons.append(data)
        response = {
            "lessons": lessons,
            "questionnaire": QuestionnaireSchema(many=False).dump(questionnaire),
            "ads": AdSchema(many=True).dump((ads)),
            "bottom_ads": AdSchema(many=True).dump((bottom_ads)),
        }
        return jsonify(response)
