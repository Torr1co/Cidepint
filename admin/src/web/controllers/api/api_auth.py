"""API Auth Controller"""
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest, HTTPException, Unauthorized

from src.dbo import institution_dbo, role_dbo, user_dbo
from src.web.utils.api import error_response
from src.web.utils.jwt import jwt_auth

auth_routing = Blueprint(
    "api_auth",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/api/auth",
)


@auth_routing.post("/")
def authenticate():
    """
    Authenticates the user and returns a JWT token
    """
    data = request.get_json()
    user = user_dbo.get_by_email(data.get("user"))

    try:
        if not user or not user.check_password(data.get("password")):
            raise BadRequest("Parametros invalidos")

        user = user_dbo.get_by_id(user.id)
        insts = institution_dbo.list_by_user_id(user.id)
        role = role_dbo.get_role(user.id)

        if not user.active or (not role and len(insts) == 0):
            raise Unauthorized("No tiene permisos para acceder a la aplicación")

        token = jwt_auth.encode({"user_id": user.id})

        return (
            jsonify({"token": token}),
            200,
            {"WWW-Authenticate": 'Basic realm="Authentication Successful"'},
        )
    except HTTPException as e:
        return error_response(e)
