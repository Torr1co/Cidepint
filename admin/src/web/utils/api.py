""" Utility functions for the API endpoints"""
from flask import Response, flash, jsonify, make_response, request
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.exceptions import HTTPException, Unauthorized

from src.web.utils.jwt import jwt_auth


def get_user_id():
    """Returns the user id from the request JWT"""
    token = request.headers.get("Authorization")
    if not token:
        return None

    token = token.split("JWT ")
    if len(token) != 2:
        return None

    data = jwt_auth.decode(token[1])
    if not data:
        return None

    return data["user_id"]


def error_response(e: HTTPException = Unauthorized("Parámetros inválidos")) -> Response:
    """
    Returns a JSON error response
    :param e: The HTTP exception to handle
    """
    return make_response(
        jsonify({"error": e.description}),
        e.code,
        {"WWW-Authenticate": 'Basic realm="Authentication Failed"'},
    )


def success_response(body: dict = None) -> Response:
    """
    Returns a JSON success response
    :param message: The message to return
    """
    if body is None:
        body = {
            "message": "Operación exitosa",
        }
    return make_response(
        jsonify(body),
        200,
    )


def response_handler(res: Response) -> Response:
    """
    Handles the response from the API endpoints
    :param res: The response to handle
    """
    if res.status_code != 200 and res.json.get("error") is not None:
        flash(res.json["error"], "error")


def load_args(data):
    args = request.args.to_dict()
    if data and isinstance(data, dict):
        for key, value in data.items():
            args[key] = value
    return ImmutableMultiDict(args)
