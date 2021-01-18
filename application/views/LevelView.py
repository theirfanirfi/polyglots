from flask_classful import FlaskView, route
from application.models.models import *
from flask import render_template, request
from application import db
from flask import redirect, url_for
from application.forms.forms import LevelForm, UpdateLevelForm
from application.utils import save_file, save_image
from werkzeug.security import generate_password_hash, check_password_hash
from application import login_manager


class LevelView(FlaskView):
    @route("/level/<int:id>", methods=["GET", "POST"])
    def level(self, id):
        form = LevelForm()
        language = Language.query.get_or_404(id)
        levels = Level.query.filter_by(language_id=id).all()
        if request.method == "POST":
            if form.validate_on_submit():
                isSaved, file_name = save_file(form.level_image.data, "level")
                new_language = Level(
                    level_name=form.level_name.data,
                    level_image=file_name,
                    language_id=language.language_id,
                )
                try:
                    db.session.add(new_language)
                    db.session.commit()
                    return redirect(url_for("LevelView:level", id=id))
                except Exception as e:
                    return "There was an issue in adding the level" + str(e)
            else:
                return render_template(
                    "level.html", form=form, levels=levels, language=language
                )
        else:
            return render_template(
                "level.html", form=form, levels=levels, language=language
            )

    @route("/update_level/<int:id>", methods=["GET", "POST"])
    def update_level(self, id):
        form = UpdateLevelForm()
        up_level = Level.query.get_or_404(id)
        language_id = up_level.language_id
        if request.method == "POST":
            if form.validate_on_submit():
                isSaved, file_name = save_file(form.level_image.data, "level")
                up_level.level_image = file_name
                up_level.level_name = form.level_name.data
                try:
                    db.session.commit()
                    return redirect(url_for("LevelView:level", id=language_id))
                except Exception as e:
                    return "There was an issue in updating the country" + str(e)
            else:
                return render_template(
                    "update_level.html", up_level=up_level, form=form
                )
        else:
            return render_template("update_level.html", up_level=up_level, form=form)

    @route("/delete_level/<int:id>")
    def delete_level(self, id):
        level_to_delete = Level.query.get_or_404(id)
        language_id = level_to_delete.language_id
        try:
            db.session.delete(level_to_delete)
            db.session.commit()
            return redirect(url_for("LevelView:level", id=language_id))
        except:
            return "There was an issue in deleting level"

    @route("/")
    def levels(self):
        levels = Level.query.all()
        return render_template("all_levels.html", levels=levels)
