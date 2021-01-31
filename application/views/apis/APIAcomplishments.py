from flask_classful import FlaskView, route
from application.models.models import Accomplishments
from flask import request
from application import db
from flask import jsonify


class APIAcomplishmentsView(FlaskView):
    @route('/save_progress', methods=['POST'])
    def save_progress(self):
        print(request.headers)
        form = request.form
        q_tags = form['q_tags']
        print(q_tags)
        if q_tags == "":
            return jsonify({'isSaved': False, 'message': "Opps, you haven't answered the questionnaire"})

        for field in form:
            if form[field] == "" or form[field] == None:
                return jsonify({'isSaved': False, 'message': 'Details are missing'})

        group_id = form['group_id']
        level_id = form['level_id']
        language_id = form['language_id']
        user_id = form['user_id']
        acp = Accomplishments.query.filter_by(group_id=group_id, level_id=level_id, language_id=language_id,
                                              user_id=user_id)
        new_acp = ""
        if acp.count() > 0:
            new_acp = acp.first()
        else:
            new_acp = Accomplishments()

        new_acp.group_id = group_id
        new_acp.level_id = level_id
        new_acp.language_id = group_id
        new_acp.user_id = user_id
        new_acp.q_tags = q_tags

        try:
            db.session.add(new_acp)
            db.session.commit()
            return jsonify({'isSaved': True, 'message': 'Progress saved'})
        except Exception as e:
            print(e)
            return jsonify({'isSaved': False, 'message': 'Error: Please try again.'})
