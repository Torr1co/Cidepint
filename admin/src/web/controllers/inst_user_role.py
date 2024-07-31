"""User Institution Role logic"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from src.dbo import configuration_dbo, inst_user_role_dbo
from src.models.enums import Operations
from src.web.utils import session as session_utils
from src.web.utils.auth import validate_operation
from src.web.utils.forms.crud import ConfirmDeleteForm
from src.web.utils.forms.inst_user_role import (
    InstitutionAddUserForm,
    UserUpdateInstRoleForm,
)

inst_user_role_routing = Blueprint(
    "inst_user_role",
    __name__,
    static_folder="static",
)


@inst_user_role_routing.get("/institution-users")
@validate_operation(Operations.INSTITUTION_USER.index)
def institution_users_page():
    """Returns all users from an institution"""
    inst_id = session_utils.get_inst_id()
    page = request.args.get("page", 1, type=int)
    per_page = configuration_dbo.get_per_page()
    users, total_pages = inst_user_role_dbo.search(
        inst_id, page=page, per_page=per_page
    )

    results = [
        {**user, "role_form": UserUpdateInstRoleForm(role=user["role"])}
        for user in users
    ]
    return render_template(
        "inst-user-roles/institution-users-index.html",
        users=results,
        page=page,
        total_pages=total_pages,
        add_form=InstitutionAddUserForm(),
        delete_form=ConfirmDeleteForm(),
    )


@inst_user_role_routing.route("/inst-user-roles/add-user", methods=["POST", "GET"])
@validate_operation(operation=Operations.INSTITUTION_USER.update)
def create_role():
    """Adds a user to an institution"""
    form = InstitutionAddUserForm(request.form)
    if request.method == "GET":
        form = InstitutionAddUserForm()
        return render_template("inst-user-roles/institution-user-add.html", form=form)
    if not form.validate():
        flash("Email invalido", "error")
        return render_template("inst-user-roles/institution-user-add.html", form=form)
    if not inst_user_role_dbo.create_new(
        session_utils.get_inst_id(), form.data.get("email"), form.data.get("role")
    ):
        flash("El usuario no existe", "error")
        return render_template("inst-user-roles/institution-user-add.html", form=form)
    flash("Usuario agregado exitosamente!", "success")
    return redirect(url_for("inst_user_role.institution_users_page"))


@inst_user_role_routing.post("/inst-user-roles/<user_id>/update-role")
@validate_operation(operation=Operations.INSTITUTION_USER.update)
def update_role(user_id):
    """
    Updates the role in the institution of the user
    :param user_id: user id
    """
    form = UserUpdateInstRoleForm(request.form)
    inst_user_role_dbo.update_role(
        user_id, session_utils.get_inst_id(), form.data.get("role")
    )

    flash("Rol actualizado exitosamente!", "success")
    return redirect(url_for("inst_user_role.institution_users_page"))


@inst_user_role_routing.post("/inst-user-roles/<user_id>/delete-role")
@validate_operation(operation=Operations.INSTITUTION_USER.delete)
def delete_role(user_id):
    """
    Deletes the role of the user in the institution
    :param user_id: user id
    """
    inst_user_role_dbo.delete_role(user_id, session_utils.get_inst_id())
    flash("Usuario eliminado de la institucion!", "success")
    return redirect(url_for("inst_user_role.institution_users_page"))
