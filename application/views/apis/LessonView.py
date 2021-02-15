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
                if s.is_straight_translation == 1 or s.is_multiple_images or s.is_write_this == 1:
                    print('working ' + str(s.is_write_this == 1) + ' ' + str(s.is_write_this))
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
        # questionnaire = Questionnaire.query.filter_by(group_id=group_id).first()

        ad_sql = text("SELECT * FROM `advertisements` WHERE ("
                      + "((advertisements.`ad_lower_limit_age` = 0) or (" + str(
            user.age) + " >= advertisements.`ad_lower_limit_age` AND " + str(
            user.age) + " <= advertisements.`ad_upper_limit_age`))"
                      + " AND (advertisements.`ad_continent` = '" + str(
            user.continent) + "' or advertisements.`ad_continent` = 'global')"
                      + " AND (advertisements.`country` = '" + str(
            user.country) + "' or advertisements.`country` = 'All')"
                      + " AND (advertisements.`ad_gender` = '" + str(
            user.gender) + "' or advertisements.`ad_gender` = 'Both')"
                      + " AND is_bottom_ad = 0)")
        ads = db.engine.execute(ad_sql)
        ads_list = list()
        if ads.rowcount > 0:
            for ad in ads:
                ad_data = dict()
                ad_data['ad'] = AdSchema(many=False).dump(ad)
                ad_ques = Questionnaire.query.filter_by(ad_id=ad.ad_id).all()
                ad_data['questionnaire'] = QuestionnaireSchema(many=True).dump(ad_ques)
                ads_list.append(ad_data)

        bottom_ad_sql = text("SELECT * FROM `advertisements` WHERE ("
                      + "((advertisements.`ad_lower_limit_age` = 0) or (" + str(
            user.age) + " >= advertisements.`ad_lower_limit_age` AND " + str(
            user.age) + " <= advertisements.`ad_upper_limit_age`))"
                      + " AND (advertisements.`ad_continent` = '" + str(
            user.continent) + "' or advertisements.`ad_continent` = 'global')"
                      + " AND (advertisements.`country` = '" + str(
            user.country) + "' or advertisements.`country` = 'All')"
                      + " AND (advertisements.`ad_gender` = '" + str(
            user.gender) + "' or advertisements.`ad_gender` = 'Both')"
                      + " AND is_bottom_ad = 1)")
        bottom_ads = db.engine.execute(bottom_ad_sql)

        if sentences.count() > 0:
            sentences = sentences.all()
            for s in sentences:
                if s.is_straight_translation == 1 or s.is_multiple_images or s.is_write_this == 1:
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
        response = {
            "lessons": lessons,
            "ads": ads_list,
            "bottom_ads": AdSchema(many=True).dump(bottom_ads),
        }
        return jsonify(response)
