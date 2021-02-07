from flask_classful import FlaskView, route
from flask import request, flash


class UpdateLessonView(FlaskView):

    @route('/sentence_translation/<int:id>', methods=['GET', 'POST'])
    def sentence_translation(self, id):
        if request.method == "GET":
            pass
        elif request.method == "POST":
            pass
        else:
            return 'invalid request'

    @route('/images_lesson/<int:id>', methods=['GET', 'POST'])
    def images_lesson(self, id):
        if request.method == "GET":
            pass
        elif request.method == "POST":
            pass
        else:
            return 'invalid request'

    @route('/single_image_lesson/<int:id>', methods=['GET', 'POST'])
    def single_image_lesson(self, id):
        if request.method == "GET":
            pass
        elif request.method == "POST":
            pass
        else:
            return 'invalid request'

    @route('/write_this/<int:id>', methods=['GET', 'POST'])
    def write_this(self, id):
        if request.method == "GET":
            pass
        elif request.method == "POST":
            pass
        else:
            return 'invalid request'

    @route('/pairs_to_match/<int:id>', methods=['GET', 'POST'])
    def pairs_to_match(self, id):
        if request.method == "GET":
            pass
        elif request.method == "POST":
            pass
        else:
            return 'invalid request'

    @route('/tap_what_you_hear/<int:id>', methods=['GET', 'POST'])
    def tap_what_you_hear(self, id):
        if request.method == "GET":
            pass
        elif request.method == "POST":
            pass
        else:
            return 'invalid request'
