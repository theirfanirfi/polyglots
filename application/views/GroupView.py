from flask_classful import FlaskView, route
from application.models.models import *
from flask import render_template, request
from application import db
from flask import redirect, url_for
from application.forms.forms import GroupForm, UpdateGroupForm
from application.utils import save_file, save_image
from werkzeug.security import generate_password_hash, check_password_hash
from application import login_manager


class GroupView(FlaskView):
    @route("/group/<int:id>", methods=["GET", "POST"])
    def group(self, id):
        form = GroupForm()
        level = Level.query.get_or_404(id)
        groups = Groups.query.filter_by(level_id=id).all()
        if request.method == "POST":
            if form.validate_on_submit():
                isSaved, file_name = save_file(form.group_image.data, "group")
                new_group = Groups(
                    group_name=form.group_name.data,
                    group_image=file_name,
                    level_id=level.level_id,
                    language_id=level.language_id,
                )
                try:
                    db.session.add(new_group)
                    db.session.commit()
                    return redirect(url_for("GroupView:group", id=id))
                except Exception as e:
                    return "There was an issue in adding the group" + str(e)
            else:
                return render_template(
                    "group.html", form=form, level=level, groups=groups
                )
        else:
            return render_template("group.html", form=form, level=level, groups=groups)

    @route("/delete_group/<int:id>")
    def delete_group(self, id):
        group_to_delete = Groups.query.get_or_404(id)
        level_id = group_to_delete.level_id
        try:
            db.session.delete(group_to_delete)
            db.session.commit()
            return redirect(url_for("GroupView:group", id=level_id))
        except:
            return "There was an issue in deleting group"

    @route("/update_group/<int:id>", methods=["GET", "POST"])
    def update_group(self, id):
        form = UpdateGroupForm()
        up_group = Groups.query.get_or_404(id)
        level_id = up_group.level_id
        if request.method == "POST":
            if form.validate_on_submit():
                isSaved, file_name = save_file(form.group_image.data, "group")
                up_group.group_image = file_name
                up_group.group_name = form.group_name.data
                try:
                    db.session.commit()
                    return redirect(url_for("GroupView:group", id=level_id))
                except Exception as e:
                    return "There was an issue in updating the group" + str(e)
            else:
                return render_template(
                    "update_group.html", up_group=up_group, form=form
                )
        else:
            return render_template("update_group.html", up_group=up_group, form=form)

    @route("/")
    def groups(self):
        groups = Groups.query.all()
        return render_template("all_groups.html", groups=groups)
