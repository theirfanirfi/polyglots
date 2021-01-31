from application import app, mail
from application.models.models import Word
import os
from werkzeug.utils import secure_filename
from flask_mail import Message


def save_file(file, type):
    file_name = secure_filename(file.filename)
    file_ext = file_name.split(".")[1]
    folder = os.path.join(app.root_path, "static/" + type + "/")
    file_path = os.path.join(folder, file_name)
    try:
        file.save(file_path)
        return True, file_name
    except:
        return False, file_name


def delete_image(file, type):
    try:
        os.remove(os.path.join(app.root_path, "static/" + type + "/" + file))
        return True
    except:
        return False


def save_image(file, type):
    image_name = secure_filename(file.filename)
    file_ext = image_name.split(".")[1]
    folder = os.path.join(app.root_path, "static/" + type + "/")
    file_path = os.path.join(folder, image_name)
    try:
        file.save(file_path)
        return True, image_name
    except:
        return False, image_name


def process_lesson(req, group):
    form = req.form
    words = form.getlist("word[]")
    print(words)
    words_meanings = form.getlist("word_meaning[]")
    words_sounds = req.files.getlist("word_sound[]")
    words_images = req.files.getlist("word_image[]")

    # sentence = form["sentence"]
    # translation = form["translation"]
    meanings = None
    sound = None
    image = None
    counter = 0
    total_words = len(words)

    for i, word in enumerate(words):
        if words_meanings[i]:
            meanings = words_meanings[i]
        else:
            continue

        if words_sounds[i]:
            iSaved, file_name = save_file(words_sounds[i], "audio")
            if iSaved:
                sound = file_name

        if words_images[i]:
            iSaved, file_name = save_file(words_images[i], "word")
            if iSaved:
                image = file_name

        isWordInserted = Word.check_word_in_db(
            word, meanings, sound, image, group.language_id
        )
        if isWordInserted:
            counter = counter + 1
    return True, counter, total_words


def send_email(user, message):
    msg = Message("Polyglots points", sender=("Polyglots points", "me@pp.com"))
    msg.recipients = ["theirfanullah@gmail.com"]
    msg.body = message
    msg.html = message
    try:
        mail.send(msg)
        print("email sent")
        return True
    except Exception as e:
        print(e)
        return False
