from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug import exceptions

from src.dbo import configuration_dbo, inst_user_role_dbo, institution_dbo
from src.models.enums import Operations, Roles
from src.schemas.institution_schema import index_institution_schema, institution_schema
from src.web.utils.auth import validate_operation
from src.web.utils.forms.crud import ConfirmDeleteForm
from src.web.utils.forms.institution import (
    InstitutionAddOwnerForm,
    InstitutionCreateForm,
    InstitutionUpdateForm,
)

institution_routing = Blueprint(
    "institutions",
    __name__,
    static_folder="static",
    template_folder="templates/institutions",
    url_prefix="/institutions",
)


@institution_routing.get("/")
@validate_operation(Operations.INSTITUTION.index)
def institution_index():
    """Returns all institutions and renders the institution page"""
    q = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    per_page = configuration_dbo.get_per_page()
    institutions = institution_dbo.search(q, page, per_page)

    return render_template(
        "institutions/institution-index.html",
        delete_form=ConfirmDeleteForm(),
        institutions=index_institution_schema.dump(institutions),
        page=page,
        total_pages=institutions.pages,
    )


@institution_routing.get("/<inst_id>")
@validate_operation(Operations.INSTITUTION.show)
def institution_show(inst_id):
    """
    Returns the institution page
    :param inst_id: institution id
    """
    current = institution_dbo.get_by_id(inst_id)
    serialized = institution_schema.dump(current)
    serialized["keywords"] = ",".join(serialized["keywords"])
    update_form = InstitutionUpdateForm(data=serialized)
    owner_form = InstitutionAddOwnerForm()
    return render_template(
        "institutions/institution-update.html",
        inst=current,
        update_form=update_form,
        owner_form=owner_form,
    )


@institution_routing.post("/<inst_id>/update")
@validate_operation(Operations.INSTITUTION.update)
def institution_update(inst_id):
    """
    Updates the institution
    :param inst_id: institution id
    """
    current = institution_dbo.get_by_id(inst_id)
    form = InstitutionUpdateForm(request.form)
    if form.validate():
        keywords = form.data["keywords"].split(",")
        keywords = [keyword.strip() for keyword in keywords]
        institution_dbo.update(
            institution=current, data={**form.data, "keywords": keywords}
        )
        flash("Institución actualizada exitosamente!", "success")
    else:
        flash("Error al actualizar la institución", "error")
    return redirect(url_for("institutions.institution_show", inst_id=inst_id))


@institution_routing.post("/<inst_id>/add-owner")
@validate_operation(operation=Operations.INSTITUTION_USER.create)
def add_owner(inst_id):
    """
    Adds a user to an institution as an owner
    :param inst_id: inst id
    """

    form = InstitutionAddOwnerForm(request.form)
    if request.method == "GET":
        form = InstitutionAddOwnerForm()
    elif not form.validate():
        flash("Email invalido", "error")
    elif not inst_user_role_dbo.create_new(
        institution_id=inst_id,
        user_email=form.data.get("email"),
        role=Roles.OWNER.value,
    ):
        flash("No se pudo asignar al usuario", "error")
    else:
        flash("Usuario agregado exitosamente!", "success")
    return redirect(url_for("institutions.institution_show", inst_id=inst_id))


@institution_routing.route("/create", methods=["GET", "POST"])
@validate_operation(Operations.INSTITUTION.create)
def institution_create():
    """Returns the institution create input page"""
    form = InstitutionCreateForm(request.form)
    # Renders the page
    if request.method == "GET":
        form = InstitutionCreateForm()
        return render_template("institutions/institution-create.html", form=form)
    # Handles the form
    if not form.validate():
        flash("Error al crear la institución", "error")
        return render_template("institutions/institution-create.html", form=form)
    new_institution = form.data
    keywords = form.data["keywords"].split(",")
    new_institution["keywords"] = [keyword.strip() for keyword in keywords]
    new_institution.pop("csrf_token")
    try:
        institution_dbo.create_new(**new_institution)
        flash("Institucion añadida exitosamente!", "success")
    except exceptions.HTTPException as exc:
        flash(exc.description, "error")
        return render_template("institutions/institution-create.html", form=form)
    return redirect(url_for("institutions.institution_index"))


@institution_routing.post("/<inst_id>/delete")
@validate_operation(Operations.INSTITUTION.delete)
def institution_delete(inst_id):
    """
    Deletes an institution
    :param inst_id: inst id
    """

    current = institution_dbo.get_by_id(inst_id)
    institution_dbo.delete(current)
    flash("Institutcion eliminada exitosamente!", "success")
    return redirect(url_for("institutions.institution_index"))
