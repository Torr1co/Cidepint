from flask import session

from src.dbo import inst_user_role_dbo, role_dbo
from src.web.utils.jwt import jwt_auth


def get_user_id():
    """Returns the current user"""
    token = session.get("jwt_token")
    data = jwt_auth.decode(token)
    return data["user_id"]


def get_inst_id():
    """Returns the current institution"""
    return session.get("institution_id")


def get_role(user_id=None, inst_id=None):
    """Returns the current role"""

    return (
        role_dbo.get_role(get_user_id())
        if not get_inst_id()
        else inst_user_role_dbo.get_role(get_user_id(), get_inst_id())
    )


def change_institution(inst_id):
    """Changes the current institution"""
    session["institution_id"] = inst_id
    session["role"] = get_role()


def set_institutions(insts):
    """Sets the institutions"""
    session["institutions"] = insts
    change_institution(insts[0].id)
