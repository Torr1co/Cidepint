from sqlalchemy.exc import SQLAlchemyError
from werkzeug import exceptions

from src.core.crypto import cipher
from src.core.database import db
from src.dbo import role_dbo
from src.models.enums import Roles
from src.models.institution_user_role import InstitutionUserRoleModel
from src.models.user import UserModel


def search_by_active(active=True):
    """Returns a list of active users"""
    return UserModel.query.filter_by(active=active).all()


def list_by_institution(inst_id):
    """Returns a list of users by institution"""
    return UserModel.query.filter(
        UserModel.id.in_(
            InstitutionUserRoleModel.query.with_entities(
                InstitutionUserRoleModel.user_id
            ).filter_by(institution_id=inst_id)
        )
    ).all()


def create_new(firstname, lastname, username, email, password):
    """Creates a new user"""
    try:
        user = UserModel(
            firstname=firstname,
            lastname=lastname,
            username=username,
            email=email,
            password=cipher.encrypt(password),
            active=True,
        )
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError as exc:
        db.session.rollback()
        raise exceptions.BadRequest("El nombre de usuario o email ya existe") from exc
    return user


def get_by_username(username):
    """Returns a user searching by username"""
    user = UserModel.query.filter_by(username=username).first()
    return user


def get_by_email(email):
    """Returns a user searching by email"""
    user = UserModel.query.filter_by(email=email).first()
    return user


def get_by_id(userid):
    """Returns a user searching by id"""
    user = UserModel.query.filter_by(id=userid).first()
    return user


def delete(user):
    """Deletes a user"""
    db.session.delete(user)
    db.session.commit()
    return user


def update(user, data):
    """Updates a user"""
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user


def search(query, active, page, per_page):
    """Returns a list of users filtering by the given params"""
    users = UserModel.query.filter(
        UserModel.email.contains(query),
        active == "all" or UserModel.active == (active == "active"),
    ).paginate(page=page, per_page=per_page, error_out=False)

    results = [
        {
            **user.serialize(),
            "can_update": role_dbo.get_role(user.id) != Roles.SUPERADMIN.value,
        }
        for user in users
    ]

    return results, users.pages
