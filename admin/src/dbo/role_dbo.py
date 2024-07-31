from src.core.database import db
from src.models.enums import Roles
from src.models.role import RoleModel, UserRoleModel


def create_roles():
    """
    Creates the operations for the app.
    """
    roles = [role.value for role in Roles]
    for role in roles:
        new_role = RoleModel(role)
        db.session.add(new_role)
        db.session.commit()


def create_new(user_id, role):
    """Creates a new user role relation"""

    new_user_role = UserRoleModel(user_id=user_id, role=role)
    db.session.add(new_user_role)
    db.session.commit()
    return new_user_role


def get_role(user_id):
    """Gets the role of a user"""
    user_role = UserRoleModel.query.filter_by(user_id=user_id).first()
    if not user_role:
        return None

    return user_role.role
