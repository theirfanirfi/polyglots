from flask_classful import FlaskView, route
from application.models.models import *
from flask import render_template, request
from application import db
from flask import redirect, url_for
from application.forms.forms import (
    CountryForm,
    UpdateCountryForm,
)
from application.utils import save_file
from application import login_manager
from sqlalchemy import text


class CountryView(FlaskView):
    @route("continent/<int:id>", methods=["GET", "POST"])
    def continent(self, id):
        form = CountryForm()
        continent = Continents.query.filter_by(continent_id=id).first()
        sql = text(
            "SELECT *, (select count(*) from language where language.country_id=countries.country_id) as total_languages FROM countries Left join continents on continents.continent_id = countries.continent_id"
        )
        countries = db.engine.execute(sql)
        if request.method == "POST":
            if form.validate_on_submit():
                isSaved, file_name = save_file(form.image.data, "Countries")
                new_country = Countries(
                    country_name=form.country_name.data,
                    country_image=file_name,
                    continent_id=id,
                )
                try:
                    db.session.add(new_country)
                    db.session.commit()
                    return redirect(url_for("CountryView:continent", id=id))
                except Exception as e:
                    return (
                        "Error occurred while adding the country. Please try again."
                        + str(e)
                    )
            else:
                return render_template(
                    "make_country.html",
                    form=form,
                    continent=continent,
                    countries=countries,
                )
        else:
            return render_template(
                "make_country.html", form=form, continent=continent, countries=countries
            )

    @route("/update_country/<int:id>", methods=["GET", "POST"])
    def update_country(self, id):
        form = UpdateCountryForm()
        up_country = Countries.query.get_or_404(id)
        continent_id = up_country.continent_id
        if request.method == "POST":
            if form.validate_on_submit():
                isSaved, file_name = save_file(form.image.data, "Countries")
                up_country.country_image = file_name
                up_country.country_name = form.country_name.data
                try:
                    db.session.commit()
                    return redirect(url_for("CountryView:continent", id=continent_id))
                except Exception as e:
                    return "There was an issue in updating the country" + str(e)
            else:
                return render_template(
                    "update_country.html", up_country=up_country, form=form
                )
        else:
            form.country_name.data = up_country.country_name
            return render_template(
                "update_country.html", up_country=up_country, form=form
            )

    @route("/delete_country/<int:id>")
    def delete_country(self, id):
        country_to_delete = Countries.query.get_or_404(id)
        continent_id = country_to_delete.continent_id
        try:
            db.session.delete(country_to_delete)
            db.session.commit()
            return redirect(url_for("CountryView:continent", id=continent_id))
        except Exception as e:
            return "There was an issue in deleting the country" + str(e)

    @route("/")
    def all_countries(self):
        countries = Countries.query.all()
        return render_template("all_countries.html", cunts=countries)
