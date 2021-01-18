from application import app, db
from flask_login import (
    UserMixin,
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(80))


class Continents(db.Model):
    continent_id = db.Column(db.Integer, primary_key=True)
    continent_name = db.Column(db.String(200), nullable=False)
    countries = db.relationship("Countries", backref="continents", lazy="dynamic")

    def __repr__(self):
        return "[Continents {}]".format(self.continent_name)

    @staticmethod
    def getContinentsForSelectField():
        conts = Continents.query.all()
        conts_s = [(cont.continent_id, cont.continent_name) for cont in conts]
        return conts_s


class Countries(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(200), nullable=False)
    country_image = db.Column(db.Text, nullable=False)
    continent_id = db.Column(db.Integer, db.ForeignKey("continents.continent_id"))
    language = db.relationship("Language", backref="countries", lazy="dynamic")

    def __repr__(self):
        return "[Countries {}]".format(self.ountry_name)

    @staticmethod
    def getCountriesForSelectField():
        count = Countries.query.all()
        count_s = [(mulk.country_id, mulk.country_name) for mulk in count]
        return count_s


class Language(db.Model):
    language_id = db.Column(db.Integer, primary_key=True)
    language_name = db.Column(db.String(200), nullable=False)
    language_image = db.Column(db.Text, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.country_id"))
    level = db.relationship("Level", backref="language", lazy="dynamic")
    group = db.relationship("Groups", backref="groups", lazy="dynamic")
    lesson = db.relationship("Lessons", backref="lessons", lazy="dynamic")
    wd = db.relationship("Word", backref="language", lazy="dynamic")

    def __repr__(self):
        return "[Language {}]".format(self.language_name)

    @staticmethod
    def getLanguagesForSelectField():
        langs = Language.query.all()
        lang_s = [(lang.language_id, lang.language_name) for lang in langs]
        return lang_s


class Level(db.Model):
    level_id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(200), nullable=False)
    level_image = db.Column(db.Text, nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey("language.language_id"))
    group = db.relationship("Groups", backref="level", lazy="dynamic")

    def __repr__(self):
        return "[Level {}]".format(self.level_name)

    @staticmethod
    def getLevelsForSelectField():
        lvl = Level.query.all()
        level_s = [(l.level_id, l.level_name) for l in lvl]
        return level_s


class Groups(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(200), nullable=False)
    group_image = db.Column(db.Text, nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey("level.level_id"))
    language_id = db.Column(db.Integer, db.ForeignKey("language.language_id"))
    lesson = db.relationship("Lessons", backref="groups", lazy="dynamic")

    def __repr__(self):
        return "[Groups {}]".format(self.group_name)

    @staticmethod
    def getGroupsForSelectField():
        groups = Groups.query.all()
        groups_s = [(group.group_id, group.group_name) for group in groups]
        return groups_s


class Lessons(db.Model):
    lesson_id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String(200), nullable=True)
    translation = db.Column(db.String(200), nullable=True)
    options_tags = db.Column(db.String(200), nullable=True)
    images = db.Column(db.String(200), nullable=True)
    sounds = db.Column(db.String(200), nullable=True)
    words_for_images = db.Column(db.String(200), nullable=True)
    is_straight_translation = db.Column(db.Integer, default=0)
    is_multiple_images = db.Column(db.Integer, default=0)
    is_single_image = db.Column(db.Integer, default=0)
    is_pairs_to_match = db.Column(db.Integer, default=0)
    is_input_base_on_voice= db.Column(db.Integer, default=0)
    is_write_this= db.Column(db.Integer, default=0)
    is_correct_character_selection= db.Column(db.Integer, default=0)
    is_tap_what_you_hear= db.Column(db.Integer, default=0)
    language_id = db.Column(db.Integer, db.ForeignKey("language.language_id"))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.group_id"))



class MultipleImages(Lessons):
    def __init__(self):
        self.is_multiple_images = 1

    @staticmethod
    def fetch_all():
        return Lessons.query.filter_by(is_multip_images=1)

class SentenceLesson(Lessons):

    def __init__(self):
        self.is_straight_translation = 1

    @staticmethod
    def fetch_all():
        return Lessons.query.filter_by(is_straight_translation=1)

class SingelImage(Lessons):

    def __init__(self):
        self.is_single_image = 1

    @staticmethod
    def fetch_all():
        return Lessons.query.filter_by(is_single_image=1)

class PairsToMatch(Lessons):
    def __init__(self):
        self.is_pairs_to_match = 1

    @staticmethod
    def fetch_all():
        return Lessons.query.filter_by(is_pairs_to_match=1)

class InputBasedOnVoice(Lessons):
    def __init__(self):
        self.is_input_base_on_voice = 1

    @staticmethod
    def fetch_all():
        return Lessons.query.filter_by(is_input_base_on_voice=1)

class WriteThisLesson(Lessons):
    def __init__(self):
        self.is_write_this = 1

    @staticmethod
    def fetch_all():
        return Lessons.query.filter_by(is_write_this=1)

class CharacterSelection(Lessons):
    def __init__(self):
        self.is_correct_character_selection = 1

    @staticmethod
    def fetch_all():
        return Lessons.query.filter_by(is_correct_character_selection=1)

class TapWhatYouHear(Lessons):
    def __init__(self):
        self.is_tap_what_you_hear = 1

    @staticmethod
    def fetch_all():
        return Lessons.query.filter_by(is_tap_what_you_hear=1)


class Word(db.Model):
    word_id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(200), nullable=False)
    word_meaning = db.Column(db.String(200), nullable=False)
    audio = db.Column(db.Text, nullable=True)
    word_image = db.Column(db.Text, nullable=True)
    language_id = db.Column(db.Integer, db.ForeignKey("language.language_id"))

    @staticmethod
    def check_word_in_db(wordd=None, meanings=None, wordAudio=None, image=None, lang_id=None):
        check = Word.query.filter_by(word=wordd, language_id=lang_id)
        if check.count() > 0:
            return False
        else:
            create_word = Word(
                word=wordd,
                word_meaning=meanings,
                word_image=image,
                audio=wordAudio,
                language_id=lang_id,
            )
            try:
                db.session.add(create_word)
                db.session.commit()
                return True
            except Exception as e:
                print("Exception: " + str(e))
                return False