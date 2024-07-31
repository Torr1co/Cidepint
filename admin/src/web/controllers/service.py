"""Service routing logic"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug import exceptions

from src.dbo import configuration_dbo, service_dbo
from src.models.enums import Operations, ServiceTypes
from src.web.utils import model as model_utils
from src.web.utils import session as session_utils
from src.web.utils.auth import validate_operation
from src.web.utils.forms.crud import ConfirmDeleteForm
from src.web.utils.forms.service import ServiceCreateForm, ServiceUpdateForm

service_routing = Blueprint(
    "services",
    __name__,
    static_folder="static",
    template_folder="templates/services",
    url_prefix="/services",
)


@service_routing.get("/")
@validate_operation(operation=Operations.SERVICE.index)
def service_index():
    """Returns all services and renders the services page"""
    query = request.args.get("q", default="")
    service_type = request.args.get("type", default="", type=ServiceTypes)
    page = request.args.get("page", default=1, type=int)
    per_page = configuration_dbo.get_per_page()
    inst_id = session_utils.get_inst_id()
    services, total_pages = service_dbo.search_by_institution(
        inst_id, query, service_type, page, per_page
    )

    return render_template(
        "services/service-index.html",
        delete_form=ConfirmDeleteForm(),
        services=services,
        page=page,
        total_pages=total_pages,
    )


@service_routing.get("/<service_id>")
@validate_operation(operation=Operations.SERVICE.show)
def service_show(service_id):
    """
    Returns the service page
    :param service_id: service id
    """
    service = service_dbo.get_by_id(service_id)
    serialized = model_utils.enum_mutation(service.serialize(), lambda x: x.name)
    serialized["keywords"] = ",".join(serialized["keywords"])
    form = ServiceUpdateForm(data=serialized)
    return render_template("services/service-update.html", service=service, form=form)


@service_routing.post("/<service_id>/update")
@validate_operation(Operations.SERVICE.update)
def service_update(service_id):
    """
    Updates a service
    :param service_id: service id
    """
    current = service_dbo.get_by_id(service_id)
    form = ServiceUpdateForm(request.form)
    if form.validate():
        keywords = form.data["keywords"].split(",")
        keywords = [keyword.strip() for keyword in keywords]
        service_dbo.update(service=current, data={**form.data, "keywords": keywords})
        flash("Servicio actualizado exitosamente!", "success")
        return redirect(url_for("services.service_index"))
    else:
        flash("Error al actualizar el servicio", "error")
        return render_template(
            "services/service-update.html", service=current, form=form
        )


@service_routing.route("/create", methods=["GET", "POST"])
@validate_operation(Operations.SERVICE.create)
def service_create():
    """Creates a new service"""
    form = ServiceCreateForm(request.form)
    if request.method == "GET":
        form = ServiceCreateForm()
        return render_template("services/service-create.html", form=form)
    # post
    if not form.validate():
        flash("Error al crear el servicio", "error")
        return render_template("services/service-create.html", form=form)
    new_service = form.data
    new_service.pop("csrf_token")
    keywords = form.data["keywords"].split(",")
    new_service["keywords"] = [keyword.strip() for keyword in keywords]
    try:
        service_dbo.create_new(**new_service, inst_id=session_utils.get_inst_id())
        flash("Servicio añadido exitosamente!", "success")
    except exceptions.HTTPException as e:
        flash(e.description, "error")
        return render_template("services/service-create.html", form=form)
    return redirect(url_for("services.service_index"))


@service_routing.post("/<service_id>/delete")
@validate_operation(Operations.SERVICE.delete)
def service_delete(service_id):
    """
    Deletes a service
    :param service_id: service id
    """
    current = service_dbo.get_by_id(service_id)
    service_dbo.delete(current)
    flash("Servicio eliminado exitosamente!", "success")
    return redirect(url_for("services.service_index"))
