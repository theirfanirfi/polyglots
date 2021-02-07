from flask_classful import FlaskView, route
from application.models.models import SentenceLesson, Groups, Lessons, MultipleImages, \
    InputBasedOnVoice, WriteThisLesson, PairsToMatch, TapWhatYouHear, Questionnaire, SingelImage
from flask import render_template, request, redirect, flash
from application import db
from flask import redirect, url_for
from application.forms.forms import LessonForm, UpdateLessonForm, QuestionnaireForm, AdsForm
from application.utils import process_lesson, save_file
from sqlalchemy import text
import json


class LessonView(FlaskView):
    # load lessons of the group
    # add lesson to the group
    @route("group/<int:id>", methods=["GET", "POST"])
    def group(self, id):
        group = Groups.query.get_or_404(id)
        lessons = SentenceLesson.query.filter_by(group_id=id).all()
        form = QuestionnaireForm()

        if request.method == "POST":
            areWordsInserted, howManyInserted, totalWords = process_lesson(request, group)
            new_lesson = SentenceLesson()
            sentence = request.form['sentence']
            new_lesson.sentence = sentence.replace(".", "")
            translation = request.form['translation']
            new_lesson.translation = translation.replace(".", "")
            new_lesson.group_id = group.group_id
            new_lesson.language_id = group.language_id
            new_lesson.real_meaning = request.form['real_meaning']
            new_lesson.secondary_meaning = request.form['secondary_meaning']
            if 'answer_to_type' in request.form:
                new_lesson.is_type_answer = 1

            new_lesson.masculine_feminine_neutral = request.form['sentence_type']
            try:
                db.session.add(new_lesson)
                db.session.commit()
                flash("Lesson Created", "info")
                # flash(str(howManyInserted)+ " words out of "+ str(totalWords)+ " added ","info")
                return redirect(request.referrer)
            except Exception as e:
                # flash(str(howManyInserted)+ " words out of "+ str(totalWords)+ " added ","info")
                flash("Error occurred in creating the lesson, please try again.", "danger")
                return redirect(request.referrer)
        else:
            sql = text(
                "SELECT *, (select count(*) FROM lessons WHERE sentence like CONCAT('%',words.word, '%')) as word_count "
                "FROM word as words WHERE language_id=" + str(group.language_id))
            # words = Word.query.filter_by(language_id=group.language_id).all()
            words = db.engine.execute(sql)
            ad_form = AdsForm()
            return render_template("lesson.html", form=form,ad_form=ad_form, lessons=lessons, group=group, words=words)

    @route("/delete_lesson/<int:id>")
    def delete_lesson(self, id):
        lesson_to_delete = SentenceLesson.query.get_or_404(id)
        group_id = lesson_to_delete.group_id
        try:
            db.session.delete(lesson_to_delete)
            db.session.commit()
            return redirect(url_for("LessonView:group", id=group_id))
        except:
            return "There was an issue in deleting lesson"

    @route("/update_lesson/<int:id>", methods=["GET", "POST"])
    def update_lesson(self, id):
        form = UpdateLessonForm()
        up_lesson = SentenceLesson.query.get_or_404(id)
        group_id = up_lesson.group_id
        if request.method == "POST":
            if form.validate_on_submit():
                up_lesson.sentence = form.sentence.data
                up_lesson.translation = form.translation.data
                try:
                    db.session.commit()
                    return redirect(url_for("LessonView:lessons", id=group_id))
                except Exception as e:
                    return "There was an issue while updating lesson" + str(e)
            else:
                return render_template(
                    "update_lesson.html", form=form, up_lesson=up_lesson
                )
        else:
            return render_template("update_lesson.html", form=form, up_lesson=up_lesson)

    @route("/")
    def lessons(self):
        # all_lessons = Lessons.query.all()
        # return render_template("all_lessons.html", all_lessons=all_lessons)
        return render_template('lessons_type.html')

    @route("/check/<string:word>/")
    def check(self, word):
        search = "%{}%".format(word)
        # sql = text("SELECT * FROM lessons WHERE AND sentence like '%"+str(word)+"%'")
        check_word = Lessons.query.filter(Lessons.sentence.like(search))
        # check_word = db.engine.execute(sql)
        return str(check_word.count())

    @route("/images_lesson", methods=['POST'])
    def images_lesson(self):
        group = Groups.query.get_or_404(request.form['group_id'])
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
        if files:
            for word, file in enumerate(files):
                isUploaded, file_name = save_file(file, 'lesson')
                if not isUploaded:
                    flash('Error occurred in uploading the image, please try again.', 'danger')
                    print('file not uploaded')
                    return redirect(request.referrer)
                images_list.append(file_name)
                if bottom_words[word] != None: words_list.append(bottom_words[word])
        else:
            flash('Error: Image must be provide.', 'danger')
            print('image must be provided')
            return redirect(request.referrer)

        new_lesson = MultipleImages()
        # new_lesson.translation =
        new_lesson.group_id = group.group_id
        new_lesson.language_id = group.language_id
        new_lesson.images = str(json.dumps(images_list))
        new_lesson.words_for_images = str(json.dumps(words_list))
        new_lesson.translation = correct_option
        new_lesson.sentence = sentence
        new_lesson.masculine_feminine_neutral = sentence_type
        print(new_lesson)
        try:
            db.session.add(new_lesson)
            db.session.commit()
            print('committed')
            flash('Lesson Created', 'info')
            return redirect(request.referrer)
        except Exception as e:
            print(e)
            flash("Error occurred in creating the lesson, please try again.", "danger")
            return redirect(request.referrer)

    @route('/sound_this_make', methods=['POST'])
    def sound_this_make(self):
        sound_file = ""
        group = Groups.query.get_or_404(request.form['group_id'])
        if not request.files:
            flash("Sound must be provided", 'danger')
            return redirect(request.referrer)

        sound_file = request.files['sound']
        tags = request.form['tags']
        if tags == None or tags == "":
            flash("Words separated by semicolon(;) must be provided", 'danger')
            return redirect(request.referrer)

        isSaved, file_name = save_file(sound_file, 'lesson')
        if not isSaved:
            flash("Sound not uploaded, please try again", 'danger')
            return redirect(request.referrer)

        new_lesson = InputBasedOnVoice()
        new_lesson.group_id = group.group_id
        new_lesson.language_id = group.language_id
        new_lesson.sounds = file_name
        new_lesson.options_tags = str(tags)
        try:
            db.session.add(new_lesson)
            db.session.commit()
            flash('Lesson added', 'info')
            return redirect(request.referrer)
        except Exception as e:
            print(e)
            flash('Error occurred in adding the lesson, please try again.', 'danger')
            return redirect(request.referrer)

    @route('/write_this', methods=['POST'])
    def write_this(self):
        group = Groups.query.get_or_404(request.form['group_id'])
        areWordsInserted, howManyInserted, totalWords = process_lesson(request, group)
        if not request.files['sound']:
            flash("Sound must be provided", 'danger')
            return redirect(request.referrer)

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

        isSaved, file_name = save_file(request.files['sound'], 'lesson')
        if not isSaved:
            flash('Sound not uploaded. Please try again.', 'danger')
            return redirect(request.referrer)

        new_lesson = WriteThisLesson()
        new_lesson.group_id = group.group_id
        new_lesson.language_id = group.language_id
        new_lesson.sentence = sentence
        new_lesson.options_tags = tags
        new_lesson.translation = correct_sentence
        new_lesson.sounds = file_name
        new_lesson.write_this_in_sentence = write_this
        new_lesson.language_id = group.language_id
        new_lesson.real_meaning = request.form['real_meaning']
        new_lesson.secondary_meaning = request.form['secondary_meaning']

        if 'answer_to_type' in request.form:
            new_lesson.is_type_answer = 1

        new_lesson.masculine_feminine_neutral = sentence_type

        try:
            db.session.add(new_lesson)
            db.session.commit()
            flash('Lesson Added.', 'info')
            return redirect(request.referrer)
        except Exception as e:
            print(e)
            flash('Error occurred in creating the lesson. Please try again.', 'danger')
            return redirect(request.referrer)

    @route('/pairs_to_match', methods=['POST'])
    def pairs_to_match(self):
        group = Groups.query.get_or_404(request.form['group_id'])
        areWordsInserted, howManyInserted, totalWords = process_lesson(request, group)
        sound = ""
        sentence = request.form['sentence']

        if sentence == None or sentence == "":
            print('Error: validation ')
            flash('Sentence must be entered.', 'danger')
            return redirect(request.referrer)

        if request.files['sound']:
            isSaved, file_name = save_file(request.files['sound'], 'lesson')
            if isSaved:
                sound = file_name

        new_lesson = PairsToMatch()
        new_lesson.group_id = group.group_id
        new_lesson.language_id = group.language_id
        new_lesson.sentence = sentence
        new_lesson.sounds = sound

        try:
            db.session.add(new_lesson)
            db.session.commit()
            flash('Lesson Added.', 'info')
            return redirect(request.referrer)
        except Exception as e:
            print(e)
            flash('Error occurred in creating the lesson. Please try again.', 'danger')
            return redirect(request.referrer)

    @route('/tap_what_you_hear', methods=['POST'])
    def tap_what_you_hear(self):
        group = Groups.query.get_or_404(request.form['group_id'])
        areWordsInserted, howManyInserted, totalWords = process_lesson(request, group)
        sound = ""
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
            sound = file_name

        new_lesson = TapWhatYouHear()
        new_lesson.group_id = group.group_id
        new_lesson.language_id = group.language_id
        new_lesson.options_tags = tags
        new_lesson.translation = correct_option
        new_lesson.sounds = sound

        try:
            db.session.add(new_lesson)
            db.session.commit()
            flash('Lesson Added.', 'info')
            return redirect(request.referrer)
        except Exception as e:
            print(e)
            flash('Error occurred in creating the lesson. Please try again.', 'danger')
            return redirect(request.referrer)

    @route('/add_questionnaire', methods=['POST'])
    def add_questionnaire(self):
        form = QuestionnaireForm()
        group = Groups.query.get_or_404(form.group_id.data)

        if form.validate_on_submit():
            check_questionnaire = Questionnaire.query.filter_by(group_id=group.group_id)
            questionnaire = ""
            if check_questionnaire.count() > 0:
                questionnaire = check_questionnaire.first()
            else:
                questionnaire = Questionnaire()

            questionnaire.group_id = group.group_id
            questionnaire.language_id = group.language_id
            questionnaire.level_id = group.level_id
            questionnaire.q_tags = form.questionnaire.data

            try:
                db.session.add(questionnaire)
                db.session.commit()
                flash('Questionnaire Added.', 'info')
                return redirect(request.referrer)
            except Exception as e:
                print(e)
                flash('Error occurred. Please try again.', 'danger')
                return redirect(request.referrer)
        else:
            return 'Validation error: Questionnaire tags must be provided.'

    @route("/single_image_lesson", methods=['POST'])
    def single_image_lesson(self):
        group = Groups.query.get_or_404(request.form['group_id'])
        areWordsInserted, howManyInserted, totalWords = process_lesson(request, group)

        file = request.files['image']
        correct_option = request.form['correct_sentence_word']
        sentence = request.form['sentence']
        sentence_type = request.form['sentence_type']
        if not file:
            flash('Select Image.', 'danger')
            return redirect(request.referrer)

        isSaved, file_name = save_file(file,'lesson')
        if not isSaved:
            flash('Error occurred. Please try again.', 'danger')
            return redirect(request.referrer)


        if correct_option == None or correct_option == "" or (sentence == None or sentence == ""):
            flash('Correct option must be provided', 'danger')
            return redirect(request.referrer)


        new_lesson = SingelImage()
        # new_lesson.translation =
        new_lesson.group_id = group.group_id
        new_lesson.language_id = group.language_id
        new_lesson.images = file_name
        new_lesson.translation = correct_option
        new_lesson.sentence = sentence
        new_lesson.is_type_answer = 1 if 'answer_to_type' in request.form else 0
        new_lesson.masculine_feminine_neutral = sentence_type
        print(new_lesson)
        try:
            db.session.add(new_lesson)
            db.session.commit()
            print('committed')
            flash('Lesson Created', 'info')
            return redirect(request.referrer)
        except Exception as e:
            print(e)
            flash("Error occurred in creating the lesson, please try again.", "danger")
            return redirect(request.referrer)

