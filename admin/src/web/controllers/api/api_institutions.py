""" API Institutions Controller Module"""
from flask import Blueprint, jsonify, make_response, request

from src.dbo import institution_dbo
from src.models.enums import Operations
from src.schemas.institution_schema import many_institution_schema

institution_routing = Blueprint(
    "api_institutions",
    __name__,
    static_folder="static",
    template_folder="templates/institutions",
    url_prefix="/api/institutions",
)


@institution_routing.get("/")
def search():
    """
    Returns all institutions according to search params q, page size and page number.
    Example URI GET https://admin-grupoXX.proyecto2023.unlp.edu.ar/api/institutions?page=2&per_page=10
    """
    q = request.args.get("q", "", type=str)
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 1, type=int)
    institutions = institution_dbo.search(q, page, per_page)

    return make_response(
        jsonify(
            {
                "data": many_institution_schema.dump(institutions),
                "page": page,
                "per_page": per_page,
                "total": institutions.total,
            }
        ),
        200,
    )
