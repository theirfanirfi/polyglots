from application import app, db, ma
from flask_login import (
    UserMixin,
)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(15), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(50), nullable=False)
    continent = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    token = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200))
    role = db.Column(db.Integer, default=0)
    is_confirmed = db.Column(db.Integer, default=0)
    confirmation_code = db.Column(db.Integer, default=0)
    reset_code = db.Column(db.Integer, default=0)
    reset_token = db.Column(db.String(200), unique=True, nullable=True)

    def get_id(self):
        return self.user_id


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "user_id",
            "fullname",
            "email",
            "gender",
            "age",
            "country_id",
            "continent_id",
            "token",
            "is_confirmed",
        )


class Continents(db.Model):
    code = db.Column(db.String(200), nullable=False, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    @staticmethod
    def getContinentsForSelectField():
        continents = Continents.query.all()
        conts_s = [(continent.code, continent.name) for continent in continents]
        return conts_s


class Countries(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    iso3 = db.Column(db.String(4), nullable=False)
    number = db.Column(db.String(4), nullable=False)
    continent_code = db.Column(db.String(4), nullable=False)
    display_order = db.Column(db.Integer, nullable=False)

    @staticmethod
    def getCountriesForSelectField():
        countries = Countries.query.all()
        count_s = [(country.name, country.name) for country in countries]
        return count_s


class CountriesSchema(ma.Schema):
    class Meta:
        fields = ("country_id", "country_name", "country_image")


class ContinentSchema(ma.Schema):
    class Meta:
        fields = ("continent_id", "continent_name")


class Advertisements(db.Model):
    ad_id = db.Column(db.Integer, primary_key=True)
    ad_name = db.Column(db.String(200), nullable=False)
    ad_image = db.Column(db.Text, nullable=False)
    ad_upper_limit_age = db.Column(db.Integer, nullable=False)
    ad_lower_limit_age = db.Column(db.Integer, nullable=False)
    ad_continent = db.Column(db.String(100), default="global")
    country = db.Column(db.String(100), default="global")
    ad_gender = db.Column(db.String(20), nullable=False)
    is_bottom_ad = db.Column(db.Integer, default=0)
    group_id = db.Column(db.Integer, default=0)
    language_id = db.Column(db.Integer, default=0)
    ad_link = db.Column(db.Text, nullable=True)

    @staticmethod
    def newAd(
            ad_name, ad_image, ad_lower_limit_age, ad_upper_limit_age,
            ad_continent, ad_gender, is_bottom_ad, ad_link,
            country, language_id
    ):
        ad = Advertisements()
        ad.ad_name = ad_name
        ad.ad_image = ad_image
        ad.ad_lower_limit_age = ad_lower_limit_age
        ad.ad_upper_limit_age = ad_upper_limit_age
        ad.ad_continent = ad_continent
        ad.ad_gender = ad_gender
        ad.country = country
        ad.language_id = language_id
        ad.ad_link = ad_link
        ad.is_bottom_ad = 1 if is_bottom_ad else 0

        return ad


class AdSchema(ma.Schema):
    class Meta:
        fields = (
            "ad_id",
            "ad_name",
            "ad_image",
            "ad_age",
            "ad_continent",
            "ad_gender",
            "is_bottom_ad",
            "ad_link",
            "ad_upper_limit_age",
            "ad_lower_limit_age",
            "country",
            "continent",
            "language_id"
        )


class Language(db.Model):
    language_id = db.Column(db.Integer, primary_key=True)
    language_name = db.Column(db.String(200), nullable=False)
    language_image = db.Column(db.Text, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.country_id"))
    level = db.relationship("Level", backref="language", lazy="dynamic")
    group = db.relationship("Groups", backref="groups", lazy="dynamic")
    lesson = db.relationship("Lessons", backref="lessons", lazy="dynamic")
    wd = db.relationship("Word", backref="language", lazy="dynamic")

    @staticmethod
    def getLanguagesForSelectField():
        langs = Language.query.all()
        lang_s = [(0, 'Any')]
        lang_s += [(lang.language_id, lang.language_name) for lang in langs]
        return lang_s


class LanguageSchema(ma.Schema):
    class Meta:
        fields = ("language_id", "language_name", "language_image")


class Level(db.Model):
    level_id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(200), nullable=False)
    level_image = db.Column(db.Text, nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey("language.language_id"))
    group = db.relationship("Groups", backref="level", lazy="dynamic")

    @staticmethod
    def getLevelsForSelectField():
        lvl = Level.query.all()
        level_s = [(l.level_id, l.level_name) for l in lvl]
        return level_s


class LevelSchema(ma.Schema):
    class Meta:
        fields = (
            "language_id",
            "level_id",
            "level_name",
            "level_image",
            "total_groups",
            "total_done",
        )


class Groups(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(200), nullable=False)
    group_image = db.Column(db.Text, nullable=False)
    is_group = db.Column(db.Integer, default=0)
    is_level = db.Column(db.Integer, default=0)
    is_lesson = db.Column(db.Integer, default=0)
    level_id = db.Column(db.Integer, db.ForeignKey("level.level_id"))
    language_id = db.Column(db.Integer, db.ForeignKey("language.language_id"))
    lesson = db.relationship("Lessons", backref="groups", lazy="dynamic")

    @staticmethod
    def getGroupsForSelectField():
        groups = Groups.query.all()
        groups_s = [(group.group_id, group.group_name) for group in groups]
        return groups_s


class GroupSchema(ma.Schema):
    class Meta:
        fields = (
            "language_id",
            "level_id",
            "group_id",
            "group_name",
            "group_image",
            "total_lessons",
        )


class Lessons(db.Model):
    lesson_id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String(200), nullable=True)
    write_this_in_sentence = db.Column(db.String(200), nullable=True)
    translation = db.Column(db.String(200), nullable=True)
    options_tags = db.Column(db.String(200), nullable=True)
    images = db.Column(db.String(200), nullable=True)
    sounds = db.Column(db.String(200), nullable=True)
    words_for_images = db.Column(db.String(200), nullable=True)
    is_straight_translation = db.Column(db.Integer, default=0)
    is_multiple_images = db.Column(db.Integer, default=0)
    is_single_image = db.Column(db.Integer, default=0)
    is_pairs_to_match = db.Column(db.Integer, default=0)
    is_input_base_on_voice = db.Column(db.Integer, default=0)
    is_write_this = db.Column(db.Integer, default=0)
    is_correct_character_selection = db.Column(db.Integer, default=0)
    is_tap_what_you_hear = db.Column(db.Integer, default=0)
    masculine_feminine_neutral = db.Column(db.String(50), default='N')
    is_type_answer = db.Column(db.Integer, default=0)
    real_meaning = db.Column(db.Text, nullable=True)
    secondary_meaning = db.Column(db.Text, nullable=True)
    language_id = db.Column(db.Integer, db.ForeignKey("language.language_id"))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.group_id"))


class Word(db.Model):
    word_id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(200), nullable=False)
    word_meaning = db.Column(db.String(200), nullable=False)
    audio = db.Column(db.Text, nullable=True)
    masculine_feminine_neutral = db.Column(db.String(50), nullable=True)
    word_image = db.Column(db.Text, nullable=True)
    language_id = db.Column(db.Integer, db.ForeignKey("language.language_id"))

    @staticmethod
    def check_word_in_db(
            wordd=None, meanings=None, wordAudio=None, image=None, lang_id=None
    ):
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


class LessonSchema(ma.Schema):
    class Meta:
        fields = (
            "lesson_id",
            "sentence",
            "translation",
            "options_tags",
            "images",
            "sounds",
            "words_for_images",
            "is_straight_translation",
            "is_multiple_images",
            "is_single_image",
            "is_pairs_to_match",
            "is_input_base_on_voice",
            "is_write_this",
            "is_correct_character_selection",
            "is_tap_what_you_hear",
            "language_id",
            "group_id",
            "masculine_feminine_neutral",
            "write_this_in_sentence",
            "is_type_answer",
            "real_meaning",
            "secondary_meaning",
        )


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


class Questionnaire(db.Model):
    __tablename__ = "questionnaires"
    q_id = db.Column(db.Integer, primary_key=True)
    q_question = db.Column(db.String(200), nullable=False)
    q_tags = db.Column(db.String(200), nullable=True)
    is_answer_to_write = db.Column(db.Integer, default=0)
    ad_id = db.Column(db.Integer, default=0)


class QuestionnaireSchema(ma.Schema):
    class Meta:
        fields = ("q_id", "q_tags","q_question","is_answer_to_write", "ad_id")


class Accomplishments(db.Model):
    acmp_id = db.Column(db.Integer, primary_key=True)
    q_tags = db.Column(db.String(200), nullable=False)
    group_id = db.Column(db.Integer, default=0)
    level_id = db.Column(db.Integer, default=0)
    lesson_id = db.Column(db.Integer, default=0)
    language_id = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, default=0)


class Settings(db.Model):
    setting_id = db.Column(db.Integer, primary_key=True)
    setting_type = db.Column(db.String(200), nullable=False)
    setting_value = db.Column(db.String(200), nullable=False)
