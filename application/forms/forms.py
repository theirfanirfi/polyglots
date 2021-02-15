from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectField,
    FileField,
    TextAreaField,
    BooleanField,
    HiddenField,
FieldList
)
from wtforms.validators import DataRequired, Email, Length, InputRequired
from application.models.models import *
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired


class QuestionnaireForm(FlaskForm):
    questionnaire = StringField(
        "Questionnaire words separated by semicolon(;)", validators=[DataRequired()]
    )
    group_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=80)]
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class SignupForm(FlaskForm):
    email = StringField(
        "email",
        validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)],
    )
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=80)]
    )
    submit = SubmitField("Sign Up")


class ContinentForm(FlaskForm):
    continent_name = StringField("Continent Name", validators=[DataRequired()])
    submit = SubmitField("Add")


class UpdateContinentForm(FlaskForm):
    continent_name = StringField("Continent Name", validators=[DataRequired()])
    submit = SubmitField("Update")


class CountryForm(FlaskForm):
    country_name = StringField("Country Name", validators=[DataRequired()])
    image = FileField("Country Image", validators=[FileAllowed(["png", "jpg", "jpeg"])])
    submit = SubmitField("Add")


class AdsForm(FlaskForm):
    ads_name = StringField("Ad Name", validators=[DataRequired()])
    ad_upper_limit_age = StringField("Age Upper Limit", validators=[DataRequired()])
    ad_lower_limit_age = StringField("Age Lower Limit", validators=[DataRequired()])
    ad_link = StringField("Ad Link", validators=[DataRequired()])

    ad_continent = StringField("Continent",validators=[DataRequired()], render_kw={'list':'continentsList'})

    ad_country = StringField("Continent Countries",render_kw={'list':'countriesList'})

    ad_languages = SelectField("Language", validators=[DataRequired()], coerce=int)

    ad_gender = SelectField(
        "Gender",
        choices=[("Male", "Male"), ("Female", "Female"), ("Both", "Both")],
        validators=[DataRequired()],
    )
    image = FileField(
        "Ad Image/Video", validators=[FileAllowed(["png", "jpg", "jpeg", "gif","mp4","avi","flv","mov","wmv"])]
    )
    is_bottom_ad = BooleanField("Is Bottom Ad?")
    submit = SubmitField("Add")


class UpdateCountryForm(FlaskForm):
    country_name = StringField("Country Name", validators=[DataRequired()])
    image = FileField("Country Image", validators=[FileAllowed(["png", "jpg", "jpeg"])])
    submit = SubmitField("Update")


class LanguageForm(FlaskForm):
    lang_name = StringField("Language Name", validators=[DataRequired()])
    lang_image = FileField(
        "Language Image", validators=[FileAllowed(["png", "jpg", "jpeg"])]
    )
    submit = SubmitField("Add")


class UpdateLanguageForm(FlaskForm):
    lang_name = StringField("Language Name", validators=[DataRequired()])
    lang_image = FileField(
        "Language Image", validators=[FileAllowed(["png", "jpg", "jpeg"])]
    )
    submit = SubmitField("Update")


class LevelForm(FlaskForm):
    level_name = StringField("Level Name", validators=[DataRequired()])
    level_image = FileField(
        "Level Image",
        validators=[
            FileAllowed(
                ["png", "jpg", "jpeg"], "JPG, PNG, JPEG files are only allowed."
            )
        ],
    )
    submit = SubmitField("Add")


class UpdateLevelForm(FlaskForm):
    level_name = StringField("Level Name", validators=[DataRequired()])
    level_image = FileField(
        "Level Image",
        validators=[
            FileAllowed(
                ["png", "jpg", "jpeg"], "JPG, PNG, JPEG files are only allowed."
            )
        ],
    )
    submit = SubmitField("Update")


class GroupForm(FlaskForm):
    group_name = StringField("Group Name", validators=[DataRequired()])
    group_image = FileField(
        "Group Image",
        validators=[
            FileAllowed(
                ["png", "jpg", "jpeg"], "JPG, PNG, JPEG files are only allowed."
            )
        ],
    )
    submit = SubmitField("Add")


class UpdateGroupForm(FlaskForm):
    group_name = StringField("Group Name", validators=[DataRequired()])
    group_image = FileField(
        "Group Image",
        validators=[
            FileAllowed(
                ["png", "jpg", "jpeg"], "JPG, PNG, JPEG files are only allowed."
            )
        ],
    )
    submit = SubmitField("Update")


class LessonForm(FlaskForm):
    sentence = StringField("Sentence", validators=[DataRequired()])
    translation = StringField("Translation", validators=[DataRequired()])
    m_f_n = SelectField("Sentence type", choices=[('N', 'Neutral'), ('M', 'Masculine'), ('F', 'Feminine')],
                        validators=[DataRequired()])
    submit = SubmitField("Add")


class UpdateLessonForm(FlaskForm):
    sentence = StringField("Sentence", validators=[DataRequired()])
    translation = StringField("Translation", validators=[DataRequired()])
    submit = SubmitField("Update")


class WordForm(FlaskForm):
    word_name = StringField("Word", validators=[DataRequired()])
    word_mean = StringField("Translation", validators=[DataRequired()])
    select_language = SelectField(
        "Select Language", choices=[], validators=[DataRequired()]
    )
    word_image = FileField(
        "Word Image", validators=[FileAllowed(["png", "jpg", "jpeg"])]
    )
    audio = FileField("Sound", validators=[FileAllowed(["mp3", "wav", "dsd", "alac"])])
    submit = SubmitField("Add")


class UpdateWordForm(FlaskForm):
    word_name = StringField("Word", validators=[DataRequired()])
    word_mean = StringField("Translation", validators=[DataRequired()])
    select_language = SelectField(
        "Select Language", choices=[], validators=[DataRequired()]
    )
    word_image = FileField(
        "Word Image", validators=[FileAllowed(["png", "jpg", "jpeg"])]
    )
    audio = FileField("Sound", validators=[FileAllowed(["mp3", "wav", "dsd", "alac"])])
    submit = SubmitField("Update")
