""" API Controller for the authenticated user profile."""
from flask import Blueprint, jsonify, make_response, request
from marshmallow import ValidationError

from src.dbo import service_dbo, service_request_dbo, user_dbo
from src.models.enums import ServiceRequestStatus
from src.schemas.request_schema import (
    create_request_note_schema,
    create_request_schema,
    get_request_note_schema,
    get_request_schema,
    get_requests_schema,
)
from src.schemas.user_schema import get_user_schema
from src.web.utils import api as api_utils
from src.web.utils import auth

me_routing = Blueprint(
    "api_me",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/api/me",
)


@me_routing.get("/profile")
@auth.token_required()
def get_profile():
    """
    Get all the information of the authenticated user profile.
    Requires Autentication
    Example URI: GET https://admin-grupoXX.proyecto2023.unlp.edu.ar/api/me/profile
    """
    user_id = api_utils.get_user_id()

    user = user_dbo.get_by_id(user_id)
    return get_user_schema.dump(user), 200


@me_routing.get("/requests")
@auth.token_required()
def get_requests():
    """
    Get the list of requests made by the authenticated user.
    Requires Autentication
    Example URI: GET https://admin-grupoXX.proyecto2023.unlp.edu.ar/api/me/requests?page=2&per_page=10
    """
    user_id = api_utils.get_user_id()

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 1, type=int)
    req = service_request_dbo.search(
        user_id=user_id,
        page=page,
        per_page=per_page,
    )
    return make_response(
        jsonify(
            {
                "data": get_requests_schema.dump(req),
                "page": page,
                "per_page": per_page,
                "total": req.total,
            }
        ),
        200,
    )


@me_routing.get("/requests/<req_id>")
@auth.token_required()
def get_request(req_id):
    """
    Get the request made by the authenticated user.
    Requires Autentication
    Example URI: GET https://admin-grupoXX.proyecto2023.unlp.edu.ar/api/me/requests/123
    """
    user_id = api_utils.get_user_id()

    req = service_request_dbo.get_by_id(req_id)
    if not req:
        return make_response(jsonify({"error": "No se encuentro el elemento"}), 404)
    if req.user_id != user_id:
        return make_response(jsonify({"error": "Parámetros inválidos"}), 400)

    return jsonify({"data": get_request_schema.dump(req)}), 200


@me_routing.post("/requests/")
@auth.token_required()
def create_request():
    """
    Loads a service request by an authenticated user.
    Requires Autentication
    Example URI: POST https://admin-grupoXX.proyecto2023.unlp.edu.ar/api/me/requests
    """
    user_id = api_utils.get_user_id()

    try:
        req = create_request_schema.load(request.get_json())
    except ValidationError as err:
        return make_response(jsonify({"error": err.messages}), 400)

    exist_service = service_dbo.get_by_id(req["service_id"])
    if not exist_service:
        return make_response(jsonify({"error": "No existe el servicio"}), 400)

    req = service_request_dbo.create_new(
        user_id=user_id,
        service_id=req["service_id"],
        title=req["title"],
        description=req["description"],
        status=ServiceRequestStatus.PENDING,
    )
    return jsonify({"data": get_request_schema.dump(req)}), 201


@me_routing.post("/requests/<req_id>/notes")
@auth.token_required()
def create_request_note(req_id):
    """
    Loads a service request notes, by an authenticated user.
    Requires Autentication
    Example URI: POST https://admin-grupoXX.proyecto2023.unlp.edu.ar/api/me/requests/123/notes
    """
    user_id = api_utils.get_user_id()

    try:
        req = create_request_note_schema.load(request.get_json())
    except ValidationError as err:
        return make_response(jsonify({"error": err.messages}), 400)

    exist_request = service_request_dbo.get_by_id(req_id)
    if not exist_request:
        return make_response(jsonify({"error": "No existe el pedido"}), 404)

    new_request = service_request_dbo.add_note(req_id, user_id, req["text"])
    return jsonify({"data": get_request_note_schema.dump(new_request)}), 201
