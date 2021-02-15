from flask_classful import FlaskView, route
from application.models.models import Advertisements, Questionnaire, Settings, \
    Continents, Countries, Language
from flask import render_template, request, flash, jsonify
from application import db
from flask import redirect, url_for
from application.forms.forms import AdsForm, AdsSettingForm
from application.utils import save_file


class AdsView(FlaskView):
    @route('/', methods=['POST','GET'])
    def index(self):
        form = AdsForm()
        s_form = AdsSettingForm()
        ads = Advertisements.query.all()
        continents = Continents.query.all()
        form.ad_languages.choices = Language.getLanguagesForSelectField()
        setting = Settings.query.filter_by(setting_type='ad')

        if setting.count() > 0 :
            s_form.show_ad_after.data = setting.first().setting_value

        if request.method == "GET":
            return render_template("ads.html", ad_form=form, ads=ads,
                                   continents=continents, s_form=s_form)
        elif request.method == "POST":
            q_form = request.form
            print(q_form)
            questionnaire_questions = q_form.getlist('questionnaire_question[]')
            questionnaire_questions_tags = q_form.getlist('questionnaire_tags[]')
            questionnaire_answer_to_write = q_form.getlist('answer_to_write[]')

            if form.validate_on_submit():
                print('validated')
                isSaved, file_name = save_file(form.image.data, "ads")
                if not isSaved:
                    return "Ad image/Video not uploaded, please try again."

                ads = Advertisements.newAd(
                    ad_name=form.ads_name.data,
                    ad_image=file_name,
                    ad_lower_limit_age=form.ad_lower_limit_age.data,
                    ad_upper_limit_age=form.ad_upper_limit_age.data,
                    ad_link=form.ad_link.data,
                    ad_continent=form.ad_continent.data,
                    ad_gender=form.ad_gender.data,
                    is_bottom_ad=form.is_bottom_ad.data,
                    country=form.ad_country.data,
                    language_id=form.ad_languages.data,
                )

                try:
                    db.session.add(ads)
                    db.session.commit()
                    print("Advertisement added added")
                    for i, question in enumerate(questionnaire_questions):
                        q = Questionnaire()
                        q.q_question = questionnaire_questions[i]
                        q.q_tags = questionnaire_questions_tags[i]
                        q.is_answer_to_write = 0 if questionnaire_answer_to_write[i] is None else 1
                        q.ad_id = ads.ad_id
                        try:
                            db.session.add(q)
                            db.session.commit()
                        except Exception as e:
                            print("Questionnaire: " + e)

                    flash("Ad added.", "success")
                    return redirect(request.referrer)
                except Exception as e:
                    print(e)
                    return str(e)
                    print("not added")
                    flash("Error occurred", "danger")
                    return redirect(request.referrer)

            else:
                print('not validate_on_submit')
                flash("Error occurred", "danger")
                return render_template("ads.html", ad_form=form, ads=ads,
                                   continents=continents, s_form=s_form)


    @route("add_ad", methods=["POST"])
    def add_ad(self):
        form = AdsForm()
        form.ad_continent.choices = Continents.getContinentsForSelectField()
        form.ad_languages.choices = Language.getLanguagesForSelectField()
        q_form = request.form

        questionnaire_questions = q_form.getlist('questionnaire_question[]')
        questionnaire_questions_tags = q_form.getlist('questionnaire_tags[]')
        questionnaire_answer_to_write = q_form.getlist('answer_to_write[]')

        if form.validate_on_submit():
            print('validated')
            isSaved, file_name = save_file(form.image.data, "ads")
            if not isSaved:
                return "Ad image/Video not uploaded, please try again."

            ads = Advertisements.newAd(
                ad_name=form.ads_name.data,
                ad_image=file_name,
                ad_lower_limit_age=form.ad_lower_limit_age.data,
                ad_upper_limit_age=form.ad_upper_limit_age.data,
                ad_link=form.ad_link.data,
                ad_continent=form.ad_continent.data,
                ad_gender=form.ad_gender.data,
                is_bottom_ad=form.is_bottom_ad.data,
                country=form.ad_country.data,
                language_id=form.language_id.data,
            )

            try:
                db.session.add(ads)
                db.session.commit()
                print("Advertisement added added")
                for i, question in enumerate(questionnaire_questions):
                    q = Questionnaire()
                    q.q_question = questionnaire_questions[i]
                    q.q_tags = questionnaire_questions_tags[i]
                    q.is_answer_to_write = 0 if questionnaire_answer_to_write[i] is None else 1
                    q.ad_id = ads.ad_id
                    try:
                        db.session.add(q)
                        db.session.commit()
                    except Exception as e:
                        print("Questionnaire: "+e)

                flash("Ad added.", "success")
                return redirect(request.referrer)
            except Exception as e:
                print(e)
                return str(e)
                print("not added")
                flash("Error occurred", "danger")
                return redirect(request.referrer)

        else:
            print('not validate_on_submit')
            flash("Error occurred", "danger")
            ads = Advertisements.query.all()
            return render_template("ads.html", ad_form=form, ads=ads)

    @route("update_ad/<int:ad_id>", methods=["GET", "POST"])
    def update_ad(self, ad_id):
        form = AdsForm()
        ad = Advertisements.query.filter_by(ad_id=ad_id)
        if not ad.count() > 0:
            return "invalid add"

        ad = ad.first()
        if request.method == "GET":
            form.ads_name.data = ad.ad_name
            form.ad_age.data = ad.ad_age
            form.ad_gender.data = ad.ad_gender
            form.ad_continent.data = ad.ad_continent
            form.is_bottom_ad.data = True if ad.is_bottom_ad == 1 else False
            form.ad_link.data = ad.ad_link
            form.image.data = url_for("static", filename="/ads/" + ad.ad_image)
            return render_template("ad_update.html", form=form, ad=ad)
        elif request.method == "POST":
            if form.validate_on_submit():
                if not form.image.data == None:
                    isSaved, file_name = save_file(form.image.data, "ads")
                    if not isSaved:
                        return "Ad image not uploaded, please try again."
                    ad.ad_image = file_name

                ad.ad_name = form.ads_name.data
                ad.ad_age = form.ad_age.data
                ad.ad_gender = form.ad_gender.data
                ad.ad_continent = form.ad_continent.data
                ad.is_bottom_ad = 1 if form.is_bottom_ad.data == True else 0

                try:
                    db.session.add(ad)
                    db.session.commit()
                    print("added")
                    flash("Ad updated.", "success")
                    return redirect(url_for("AdsView:index"))
                except Exception as e:
                    print(e)
                    print("not added")
                    flash("Error occurred", "danger")
                    return redirect(url_for("AdsView:index"))

            else:
                return render_template("ad_update.html", form=form, ad=ad)

    @route("/delete_ad/<int:id>")
    def delete_ad(self, id):
        ad = Advertisements.query.get_or_404(id)
        try:
            db.session.delete(ad)
            db.session.commit()
            flash("Ad deleted.", "success")
            return redirect(url_for("AdsView:index"))
        except:
            flash("Error occurred in deleting the ad. Please try again.", "danger")
            return redirect(url_for("AdsView:index"))

    @route("/get_continent_countries")
    def get_continent_countries(self):
        code = request.args.get("code")

        if code is None or code == "":
            return str('Invalid code')

        countries = Countries.query.filter_by(continent_code=code).all()
        data = list()
        for c in countries:
            country = dict()
            country['code'] = c.code
            country['name'] = c.name
            data.append(country)

        return jsonify(data)

    @route('/update_ad_setting', methods=['GET', 'POST'])
    def update_ad_setting(self):
        form = AdsSettingForm()
        setting = Settings.query.filter_by(setting_type='ad')
        if setting.count() > 0 :
            setting = setting.first()
        else:
            setting = Settings()

        if request.method == "POST":
            if form.validate_on_submit():
                setting.setting_type = 'ad'
                setting.setting_value = form.show_ad_after.data

                try:
                    db.session.add(setting)
                    db.session.commit()
                    return redirect(request.referrer)
                except Exception as e:
                    print(e)
                    return redirect(request.referrer)
            else:
                return 'invalid request'
        else:
            return 'invalid request'

