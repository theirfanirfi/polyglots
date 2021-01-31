from flask_classful import FlaskView, route
from application.models.models import *
from flask import render_template, request
from application import db
from flask import redirect, url_for
from application.forms.forms import ContinentForm, UpdateContinentForm, CountryForm
from application.utils import save_file, save_image
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user
from application import login_manager


class ContinentView(FlaskView):
    @route("/", methods=["GET", "POST"])
    @login_required
    def continents(self):
        form = ContinentForm()
        if request.method == "POST":
            if form.validate_on_submit():
                new_continent = Continents(continent_name=form.continent_name.data)
                try:
                    db.session.add(new_continent)
                    db.session.commit()
                    return redirect(url_for("ContinentView:continents"))
                except:
                    return (
                        "Error occurred while adding the continent. Please try again."
                    )
            else:
                return render_template(
                    "continents.html", form=form, name=current_user.fullname
                )
        else:
            continents = Continents.query.all()
            return render_template(
                "continents.html",
                form=form,
                continents=continents,
                name=current_user.fullname,
            )

    @route("/delete_continent/<int:id>")
    def delete_continent(self, id):
        continent = Continents.query.get_or_404(id)
        try:
            db.session.delete(continent)
            db.session.commit()
            return redirect(url_for("ContinentView:continents"))
        except:
            return "Error occurred, while deleting the continent. Please try again."

    @route("/update_continent/<int:id>", methods=["GET", "POST"])
    def update_continent(self, id):
        continent = Continents.query.get_or_404(id)
        form = UpdateContinentForm()
        if request.method == "POST":
            if form.validate_on_submit():
                continent.continent_name = form.continent_name.data
                try:
                    db.session.add(continent)
                    db.session.commit()
                    return redirect(url_for("ContinentView:continents"))
                except:
                    return "Error occurred in updating the continent. Please try again."
            else:
                return render_template(
                    "cont_updated.html", continent=continent, form=form
                )
        else:
            return render_template("cont_updated.html", continent=continent, form=form)
