from sqlalchemy.exc import SQLAlchemyError
from werkzeug import exceptions

from src.core.database import db
from src.dbo import user_dbo
from src.models.simple_user import SimpleUserModel


def list_all():
    """Returns all simple users"""
    simple_users = SimpleUserModel.query.all()
    return simple_users


def create_new(firstname, lastname, email):
    """Creates a new simple user"""
    if user_dbo.get_by_email(email):
        raise exceptions.BadRequest("El email ya existe")
    try:
        simple_user = SimpleUserModel(
            firstname=firstname,
            lastname=lastname,
            email=email,
        )
        db.session.add(simple_user)
        db.session.commit()
    except SQLAlchemyError as exc:
        db.session.rollback()
        raise exceptions.BadRequest("El email ya existe") from exc
    return simple_user


def get_by_email(email):
    """Returns a simple user searching by email"""
    simple_user = SimpleUserModel.query.filter_by(email=email).first()
    return simple_user


def get_by_id(userid):
    """Returns a simple user searching by id"""
    simple_user = SimpleUserModel.query.filter_by(id=userid).first()
    return simple_user


def delete(simple_user):
    """Deletes a simple user"""
    db.session.delete(simple_user)
    db.session.commit()
    return simple_user
