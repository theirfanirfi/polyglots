from flask_classful import FlaskView, route
from flask import request, flash, redirect, url_for, render_template
from application import app, db
from application.utils import process_lesson, save_file
from application.models.models import *
from application.forms.forms import LessonForm


class UpdateLessonView(FlaskView):

    @route('/sentence_translation/<int:id>', methods=['GET', 'POST'])
    def sentence_translation(self, id):
        form = LessonForm()
        lesson = SentenceLesson.query.get_or_404(id)
        group = Groups.query.get_or_404(lesson.group_id)
        if request.method == "GET":
            # request.form['sentence'] = "wow"
            return render_template("update_lessons/sentence_translation_lesson.html",
                                   group=group,
                                   form=form,
                                   lesson=lesson)
        elif request.method == "POST":
            areWordsInserted, howManyInserted, totalWords = process_lesson(request, group)
            sentence = request.form['sentence']
            lesson.sentence = sentence.replace(".", "")
            translation = request.form['translation']
            lesson.translation = translation.replace(".", "")
            lesson.group_id = group.group_id
            lesson.language_id = group.language_id
            lesson.real_meaning = request.form['real_meaning']
            lesson.secondary_meaning = request.form['secondary_meaning']
            if 'answer_to_type' in request.form:
                lesson.is_type_answer = 1

            lesson.masculine_feminine_neutral = request.form['sentence_type']
            try:
                db.session.add(lesson)
                db.session.commit()
                flash("Lesson Updated", "info")
                # flash(str(howManyInserted)+ " words out of "+ str(totalWords)+ " added ","info")
                return redirect(request.referrer)
            except Exception as e:
                # flash(str(howManyInserted)+ " words out of "+ str(totalWords)+ " added ","info")
                flash("Error occurred in updating the lesson, please try again.", "danger")
                return redirect(request.referrer)
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
        form = LessonForm()
        lesson = WriteThisLesson.query.get_or_404(id)
        group = Groups.query.get_or_404(lesson.group_id)
        if request.method == "GET":
            # request.form['sentence'] = "wow"
            return render_template("update_lessons/write_this.html",
                                   group=group,
                                   form=form,
                                   lesson=lesson)
        elif request.method == "POST":
            group = Groups.query.get_or_404(request.form['group_id'])
            areWordsInserted, howManyInserted, totalWords = process_lesson(request, group)
            correct_sentence = request.form['correct_sentence']
            sentence = request.form['sentence']
            tags = request.form['tags']
            write_this = request.form['write_this']
            sentence_type = request.form['sentence_type']

            if correct_sentence == None or correct_sentence == "" or (sentence == None or sentence == "") or (
                    tags == None or tags == ""):
                print('Error: validation ')
                flash('All input fields are required.', 'danger')
                return redirect(request.referrer)

            if request.files['sound']:
                isSaved, file_name = save_file(request.files['sound'], 'lesson')
                if not isSaved:
                    flash('Sound not uploaded. Please try again.', 'danger')
                    return redirect(request.referrer)
                lesson.sounds = file_name

            lesson.group_id = group.group_id
            lesson.language_id = group.language_id
            lesson.sentence = sentence
            lesson.options_tags = tags
            lesson.translation = correct_sentence
            lesson.write_this_in_sentence = write_this
            lesson.language_id = group.language_id
            lesson.real_meaning = request.form['real_meaning']
            lesson.secondary_meaning = request.form['secondary_meaning']

            if 'answer_to_type' in request.form:
                lesson.is_type_answer = 1

            lesson.masculine_feminine_neutral = sentence_type

            try:
                db.session.add(lesson)
                db.session.commit()
                flash('Lesson Update.', 'info')
                return redirect(request.referrer)
            except Exception as e:
                print(e)
                flash('Error occurred in updating the lesson. Please try again.', 'danger')
                return redirect(request.referrer)
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
