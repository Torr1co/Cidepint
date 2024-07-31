""" API Institutions Controller Module"""
from flask import Blueprint, jsonify, make_response

from src.dbo import institution_dbo, service_dbo
from src.schemas.institution_schema import institution_analisis_schema
from src.schemas.service_schema import (
    service_analisis_schema,
    service_types_analisis_schema,
)

analisis_routing = Blueprint(
    "api_analisis",
    __name__,
    static_folder="static",
    url_prefix="/api/analisis",
)


@analisis_routing.get("/institutions/ranking")
def institution_time_resolution():
    """Returns the 10 institutions with best
    time resolution(time since a request is created until it is finished)."""
    institutions = institution_dbo.rank_by_time_resolution()
    return make_response(
        jsonify({"data": institution_analisis_schema.dump(institutions)}), 200
    )


@analisis_routing.get("/services/ranking")
def services_more_requested():
    """Returns the services ordered by requests."""
    services = service_dbo.rank_by_requests()
    return make_response(jsonify({"data": service_analisis_schema.dump(services)}), 200)


@analisis_routing.get("/services/types")
def services_types():
    """Returns all service request grouped by service type"""
    types = service_dbo.requests_by_type()
    return make_response(
        jsonify({"data": service_types_analisis_schema.dump(types)}), 200
    )
