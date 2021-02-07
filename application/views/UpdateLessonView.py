from flask_classful import FlaskView, route
from flask import request, flash, redirect, url_for, render_template, jsonify
from application import app, db
from application.utils import process_lesson, save_file
from application.models.models import *
from application.forms.forms import LessonForm
import json


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
        form = LessonForm()
        lesson = TapWhatYouHear.query.get_or_404(id)
        group = Groups.query.get_or_404(lesson.group_id)
        images = json.loads(lesson.images)
        images_words = json.loads(lesson.words_for_images)
        print(images_words)

        if request.method == "GET":
            return render_template("update_lessons/four_images_lesson.html",
                                   group=group,
                                   form=form,
                                   lesson=lesson, images=images, words=images_words)
        elif request.method == "POST":
            areWordsInserted, howManyInserted, totalWords = process_lesson(request, group)

            files = request.files.getlist('image[]')
            bottom_words = request.form.getlist('bottom_word[]')
            correct_option = request.form['correct_option']
            sentence = request.form['sentence']
            sentence_type = request.form['sentence_type']

            if correct_option == None or correct_option == "" or (sentence == None or sentence == ""):
                print('correct option')
                flash('Correct option must be provided', 'danger')
                return redirect(request.referrer)

            images_list = list()
            words_list = list()
            print(len(files))
            if files:
                for file in files:
                    if file:
                        isUploaded, file_name = save_file(file, 'lesson')
                        if not isUploaded:
                            flash('Error occurred in uploading the image, please try again.', 'danger')
                            print('file not uploaded')
                            return redirect(request.referrer)
                        images_list.append(file_name)
                lesson.images = str(json.dumps(images_list))

            if bottom_words:
                for word in bottom_words:
                    words_list.append(word)
                lesson.words_for_images = str(json.dumps(words_list))

            lesson.translation = correct_option
            lesson.sentence = sentence
            lesson.masculine_feminine_neutral = sentence_type
            try:
                db.session.add(lesson)
                db.session.commit()
                print('committed')
                flash('Lesson Update', 'info')
                return redirect(request.referrer)
            except Exception as e:
                print(e)
                flash("Error occurred in updating the lesson, please try again.", "danger")
                return redirect(request.referrer)
        else:
            return 'invalid request'

    @route('/single_image_lesson/<int:id>', methods=['GET', 'POST'])
    def single_image_lesson(self, id):
        form = LessonForm()
        lesson = SentenceLesson.query.get_or_404(id)
        group = Groups.query.get_or_404(lesson.group_id)
        if request.method == "GET":
            # request.form['sentence'] = "wow"
            return render_template("update_lessons/single_image_lesson.html",
                                   group=group,
                                   form=form,
                                   lesson=lesson)
        elif request.method == "POST":
            # areWordsInserted, howManyInserted, totalWords = process_lesson(request, group)
            file = request.files['image']
            correct_option = request.form['correct_sentence_word']
            sentence = request.form['sentence']
            sentence_type = request.form['sentence_type']
            if correct_option == None or correct_option == "" or (sentence == None or sentence == ""):
                flash('Correct option must be provided', 'danger')
                return redirect(request.referrer)

            if file:
                isSaved, file_name = save_file(file, 'lesson')
                if not isSaved:
                    flash('Error occurred. Please try again.', 'danger')
                    return redirect(request.referrer)
                lesson.images = file_name

            lesson.translation = correct_option
            lesson.sentence = sentence
            lesson.is_type_answer = 1 if 'answer_to_type' in request.form else 0
            lesson.masculine_feminine_neutral = sentence_type
            try:
                db.session.add(lesson)
                db.session.commit()
                print('committed')
                flash('Lesson Updated', 'info')
                return redirect(request.referrer)
            except Exception as e:
                print(e)
                flash("Error occurred in updating the lesson, please try again.", "danger")
                return redirect(request.referrer)
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
        form = LessonForm()
        lesson = PairsToMatch.query.get_or_404(id)
        group = Groups.query.get_or_404(lesson.group_id)
        if request.method == "GET":
            return render_template("update_lessons/pairs_to_match.html",
                                   group=group,
                                   form=form,
                                   lesson=lesson)
        elif request.method == "POST":
            areWordsInserted, howManyInserted, totalWords = process_lesson(request, group)
            sentence = request.form['sentence']
            if sentence == None or sentence == "":
                print('Error: validation ')
                flash('Sentence must be entered.', 'danger')
                return redirect(request.referrer)

            if request.files['sound']:
                isSaved, file_name = save_file(request.files['sound'], 'lesson')
                if isSaved:
                    lesson.sounds = file_name

            lesson.group_id = group.group_id
            lesson.language_id = group.language_id
            lesson.sentence = sentence

            try:
                db.session.add(lesson)
                db.session.commit()
                flash('Lesson Updated.', 'info')
                return redirect(request.referrer)
            except Exception as e:
                print(e)
                flash('Error occurred in updating the lesson. Please try again.', 'danger')
                return redirect(request.referrer)
        else:
            return 'invalid request'

    @route('/tap_what_you_hear/<int:id>', methods=['GET', 'POST'])
    def tap_what_you_hear(self, id):
        form = LessonForm()
        lesson = TapWhatYouHear.query.get_or_404(id)
        group = Groups.query.get_or_404(lesson.group_id)
        if request.method == "GET":
            return render_template("update_lessons/tap_what_you_hear.html",
                                   group=group,
                                   form=form,
                                   lesson=lesson)
        elif request.method == "POST":
            correct_option = request.form['correct_option']
            tags = request.form['tags']

            if correct_option == None or correct_option == "":
                print('Error: validation ')
                flash('correct option must be entered.', 'danger')
                return redirect(request.referrer)


            if request.files['sound']:
                isSaved, file_name = save_file(request.files['sound'], 'lesson')
                if not isSaved:
                    flash('Sound not uploaded. Please try again.', 'danger')
                    return redirect(request.referrer)
                lesson.sounds = file_name

            lesson.group_id = group.group_id
            lesson.language_id = group.language_id
            lesson.options_tags = tags
            lesson.translation = correct_option

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
