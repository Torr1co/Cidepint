"""API Services Controller"""
from flask import Blueprint, jsonify, make_response, request

from src.dbo import institution_dbo, service_dbo
from src.models.enums import ServiceTypes
from src.schemas.service_schema import get_service_schema, get_services_schema
from src.web.utils import auth

service_routing = Blueprint(
    "api_services",
    __name__,
    static_folder="static",
    template_folder="templates/services",
    url_prefix="/api/services",
)


# /api/services/search{?q,type,page,per_page}
@service_routing.get("/search")
def services_search():
    # TODO: Complete docstring
    """
    Returns all services by the search param
    Example URI: GET
    """
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=1, type=int)
    q = request.args.get("q", default="", type=str)
    service_type = request.args.get("type", default=None, type=str)
    try:
        service_type = ServiceTypes(service_type).name
    except (KeyError, ValueError):
        service_type = None

    services = service_dbo.search(
        q=q,
        service_type=service_type,
        page=page,
        per_page=per_page,
    )

    return make_response(
        jsonify(
            {
                "data": get_services_schema.dump(services),
                "page": page,
                "per_page": per_page,
                "total": services.total,
            },
        ),
        200,
    )


@service_routing.route("/<service_id>", methods=["GET"])
@auth.token_required()
def get_service(service_id):
    """
    Get the service with the given id.
    Example URI: GET https://admin-grupoXX.proyecto2023.unlp.edu.ar/api/services/123
    """
    service = service_dbo.get_by_id(service_id)
    if not service:
        return make_response(jsonify({"error": "Servicio no encontrado"}), 404)

    laboratory = institution_dbo.get_by_id(service.institution_id)
    service.laboratory = laboratory.name
    return make_response(jsonify(get_service_schema.dump(service)), 200)
