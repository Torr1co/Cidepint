from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from src.dbo import service_request_dbo, user_dbo
from src.models.enums import Operations
from src.web.utils import session as session_utils
from src.web.utils.auth import validate_operation
from src.web.utils.forms.service_request import (
    ServiceRequestCreateForm,
    ServiceRequestNoteForm,
    ServiceRequestSearchForm,
    ServiceRequestUpdateForm,
)

service_request_routing = Blueprint(
    "service_request",
    __name__,
    static_folder="static",
    template_folder="templates/service_requests",
)


@service_request_routing.get("/service_requests")
@validate_operation(Operations.SERVICE_REQUEST.index)
def service_request_index():
    """Returns all service_requests and renders the service_request page"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 1, type=int)
    search_form = ServiceRequestSearchForm(
        user_id=request.args.get("user_id", None),
        creation_date_start=request.args.get(
            "creation_date_start", None, type=datetime.fromisoformat
        ),
        creation_date_end=request.args.get(
            "creation_date_end", None, type=datetime.fromisoformat
        ),
        service_type=request.args.get("service_type", None),
        status=request.args.get("status", None),
    )
    users = [
        (user.id, user.username)
        for user in user_dbo.list_by_institution(session_utils.get_inst_id())
    ]
    search_form.user_id.choices = [("", "Todos"), *users]

    form_data = search_form.data
    form_data.pop("csrf_token")
    service_requests, total_pages = service_request_dbo.search_by_user(
        **form_data,
        inst_id=session_utils.get_inst_id(),
        page=page,
        per_page=per_page,
    )
    return render_template(
        "service_requests/service_request-index.html",
        page=page,
        total_pages=total_pages,
        service_requests=service_requests,
        search_form=search_form,
    )


@service_request_routing.get("/service_requests/<req_id>")
@validate_operation(Operations.SERVICE_REQUEST.show)
def service_request_show(req_id):
    """Return the service_request page"""
    service_request = service_request_dbo.get_realted_by_id(req_id)
    notes = service_request_dbo.get_notes_by_req(req_id)

    return render_template(
        "service_requests/service_request-show.html",
        service_request=service_request,
        notes=notes,
    )


@service_request_routing.route(
    "/service_requests/<req_id>/update", methods=["GET", "POST"]
)
@validate_operation(Operations.SERVICE_REQUEST.update)
def service_request_update(req_id):
    """Updates the service_request"""

    update_form = ServiceRequestUpdateForm(request.form)
    note_form = ServiceRequestNoteForm()
    service_request = service_request_dbo.get_related_by_id(req_id)

    if service_request is None:
        flash("Error al encontrar el pedido", "error")
        return redirect(url_for("service_request.service_request_index"))

    if request.method == "GET":
        update_form = ServiceRequestUpdateForm(status=service_request["status"].name)
        return render_template(
            "service_requests/service_request-update.html",
            service_request=service_request,
            update_form=update_form,
            note_form=note_form,
        )
    # post
    if not update_form.validate():
        flash("Error al crear el pedido", "error")
        return render_template(
            "service_requests/service_request-update.html",
            update_form=update_form,
            service_request=service_request,
            note_form=note_form,
        )
    service_request_dbo.update(req_id, status=update_form.data["status"])
    flash("Pedido añadido exitosamente!", "success")
    return redirect(url_for("service_request.service_request_index"))


@service_request_routing.post("/service_requests/<req_id>/notes/create")
@validate_operation(Operations.SERVICE_REQUEST.update)
def service_request_add_note(req_id):
    """
    Add a note to the request
    :param req_id: req id
    """
    note_form = ServiceRequestNoteForm(request.form)
    service_request_dbo.add_note(
        req_id=req_id,
        author_id=session_utils.get_user_id(),
        note=note_form.data["note"],
    )
    flash("Nota añadida exitosamente!", "success")
    return redirect(url_for("service_request.service_request_index"))


@service_request_routing.route("/service_requests/create", methods=["GET", "POST"])
@validate_operation(Operations.SERVICE_REQUEST.create)
def service_request_create():
    """Returns the service_request page"""
    form = ServiceRequestCreateForm(request.form)
    if request.method == "GET":
        form = ServiceRequestCreateForm()
        return render_template(
            "service_requests/service_request-create.html", form=form
        )
    # post
    if not form.validate():
        flash("Error al crear el pedido", "error")
        return render_template(
            "service_requests/service_request-create.html", form=form
        )
    new_service_request = form.data
    new_service_request.pop("csrf_token")
    service_request_dbo.create_new(**new_service_request)
    flash("Pedido añadido exitosamente!", "success")
    return redirect(url_for("service_requests.service_requests_page"))
