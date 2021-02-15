from flask_classful import FlaskView, route
from application.models.models import *
from flask import render_template, request
from application import db
from flask import redirect, url_for
from application.forms.forms import LanguageForm, UpdateLanguageForm
from application.utils import save_file, save_image
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    login_required,
    logout_user,
    current_user,
)
from application import login_manager


class LanguageView(FlaskView):
    @route("/language", methods=["GET", "POST"])
    def language(self):
        form = LanguageForm()
        languages = Language.query.all()
        if request.method == "POST":
            if form.validate_on_submit():
                isSaved, file_name = save_file(form.lang_image.data, "language")
                new_language = Language(
                    language_name=form.lang_name.data,
                    language_image=file_name,
                )
                try:
                    db.session.add(new_language)
                    db.session.commit()
                    return redirect(url_for("LanguageView:language", id=id))
                except Exception as e:
                    return "There was an issue in adding the language" + str(e)
            else:
                return render_template(
                    "all_languages.html", form=form, languages=languages
                )
        else:
            return render_template(
                "all_languages.html", form=form, languages=languages
            )

    @route("/delete_language/<int:id>")
    def delete_language(self, id):
        lang_to_delete = Language.query.get_or_404(id)
        try:
            db.session.delete(lang_to_delete)
            db.session.commit()
            return redirect(
                url_for("LanguageView:language", id=lang_to_delete.country_id)
            )
        except:
            return "There was an issue in deleting language"

    @route("/update_language/<int:id>", methods=["GET", "POST"])
    def update_language(self, id):
        form = UpdateLanguageForm()
        up_language = Language.query.get_or_404(id)
        country_id = up_language.country_id
        if request.method == "POST":
            if form.validate_on_submit():
                isSaved, file_name = save_file(form.lang_image.data, "language")
                up_language.language_image = file_name
                up_language.language_name = form.lang_name.data
                try:
                    db.session.commit()
                    return redirect(url_for("LanguageView:language", id=country_id))
                except Exception as e:
                    return "There was an issue in updating the country" + str(e)
            else:
                return render_template(
                    "update_language.html", up_language=up_language, form=form
                )
        else:
            form.lang_name.data = up_language.language_name
            return render_template(
                "update_language.html", up_language=up_language, form=form
            )

    @route("/")
    def languages(self):
        languages = Language.query.all()
        form = LanguageForm()
        return render_template("all_languages.html",
                               form=form,
                               languages=languages)
