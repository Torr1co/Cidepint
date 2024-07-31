"""User routing logic"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug import exceptions

from src.dbo import configuration_dbo, role_dbo, simple_user_dbo, user_dbo
from src.models.enums import Operations, Roles
from src.web.utils import model as model_utils
from src.web.utils import session as session_utils
from src.web.utils.auth import is_logged_in, login_required, validate_operation
from src.web.utils.forms.auth import ConfirmRegisterForm
from src.web.utils.forms.crud import ConfirmDeleteForm
from src.web.utils.forms.user import UserUpdateForm

user_routing = Blueprint(
    "users",
    __name__,
    static_folder="static",
    template_folder="templates/users",
    url_prefix="/users",
)


@user_routing.get("/")
@validate_operation(operation=Operations.USER.index)
def user_index():
    """
    Returns all users and renders the users page
    """
    per_page = configuration_dbo.get_per_page()
    page = request.args.get("page", 1, type=int)
    query = request.args.get("search", "")
    active = request.args.get("active", "all")
    users, total = user_dbo.search(
        query=query, active=active, page=page, per_page=per_page
    )

    return render_template(
        "users/user-index.html",
        delete_form=ConfirmDeleteForm(),
        users=users,
        page=page,
        total_pages=total,
    )


@user_routing.get("/<user_id>")
@validate_operation(operation=Operations.USER.show)
def user_page(user_id):
    """
    Returns the user page
    :param user_id: user id
    """
    if role_dbo.get_role(user_id) == Roles.SUPERADMIN.value:
        return redirect(url_for("users.user_index"))
    user = user_dbo.get_by_id(user_id)
    serialized = model_utils.enum_mutation(user.serialize(), lambda x: x.name)
    form = UserUpdateForm(data=serialized)
    return render_template("users/user-update.html", user=user, form=form)


@user_routing.post("/update/<user_id>")
@validate_operation(operation=Operations.USER.update)
def user_update(user_id):
    """
    Updates the user
    :param user_id: user id
    """
    current = user_dbo.get_by_id(user_id)
    form = UserUpdateForm(request.form)

    user_dbo.update(user=current, data=form.data)
    flash("Usuario actualizado exitosamente!", "success")
    return redirect(url_for("users.user_index"))


@user_routing.post("/<user_id>/delete")
@validate_operation(Operations.USER.delete)
def user_delete(user_id):
    """
    Deletes an user
    :param user_id: user id
    """

    current = user_dbo.get_by_id(user_id)
    user_dbo.delete(current)
    flash("Usuario eliminado exitosamente!", "success")
    return redirect(url_for("users.user_index"))


@user_routing.get("/confirm/<user_id>")
def confirm_page(user_id):
    """
    Returns the confirmation page
    :param user_id: user id
    """
    return render_template("confirm.html", user_id=user_id, form=ConfirmRegisterForm())


@user_routing.post("/confirm/<user_id>")
def confirm_user(user_id):
    """
    Confirms a user registration (complete registration).
    If correct, creates a new user and deletes the temp user,
    then redirects with success to login.
    :param user_id: user id
    """
    simpleuser = simple_user_dbo.get_by_id(user_id)
    try:
        user_dbo.create_new(
            firstname=simpleuser.firstname,
            lastname=simpleuser.lastname,
            username=request.form["username"],
            email=simpleuser.email,
            password=request.form["password"],
        )
        simple_user_dbo.delete(simpleuser)
        flash("Usuario confirmado exitosamente!", "success")
    except exceptions.HTTPException as error:
        flash(error.description, "error")
        return redirect(url_for("users.confirm_page", user_id=user_id))
    return redirect(url_for("auth.login_page"))


@user_routing.post("/change-institution")
@login_required
def change_institution():
    """
    Changes the institution of the authenticated user.
    Requires Autentication
    Example URI: GET https://admin-grupoXX.proyecto2023.unlp.edu.ar/api/me/change-institution
    """
    if (
        is_logged_in()
        and session_utils.get_role() != Roles.SUPERADMIN.value
        and request.form.get("inst_id")
    ):
        session_utils.change_institution(int(request.form.get("inst_id")))
    return redirect(url_for("home.home_page"))
