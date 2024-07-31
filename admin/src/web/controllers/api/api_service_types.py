"""API Services Types Controller"""
from flask import Blueprint, jsonify, request

from src.dbo import service_dbo
from src.web.utils import auth

service_types_routing = Blueprint(
    "api_service_types",
    __name__,
    static_folder="static",
    template_folder="templates/services",
    url_prefix="/api/service-types",
)


@service_types_routing.get("/")
def get_services_types():
    """
    Get a list of enabled types, filtered by the search criteria.
    Example URI: GET https://admin-grupoXX.proyecto2023.unlp.edu.ar/api/services-types
    """
    if not auth.is_logged_in():
        return jsonify({"error": "Parámetros inválidos"}), 400
    types = service_dbo.search_types(
        inst_id=request.args.get("institution", ""), q=request.args.get("q", "")
    )
    return jsonify({"data": types}), 200
