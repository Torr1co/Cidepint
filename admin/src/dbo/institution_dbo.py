from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from werkzeug import exceptions

from src.core.database import db
from src.models.institution import InstitutionModel
from src.models.institution_user_role import InstitutionUserRoleModel
from src.models.service import ServiceModel
from src.models.service_request import ServiceRequestModel


def search(q, page, per_page):
    """Returns all Institutions by keywords"""
    return InstitutionModel.query.filter(
        func.array_to_string(InstitutionModel.keywords, ",").ilike(
            func.any_(["%" + q + "%"])
        )
    ).paginate(page=page, per_page=per_page, error_out=False)


def list_all():
    """Returns all Institutions"""
    insts = InstitutionModel.query.all()
    return insts


def list_by_keyword(keyword):
    """Returns all Institutions by keywords"""
    insts = InstitutionModel.query.filter(
        func.array_to_string(InstitutionModel.keywords, ",").ilike(
            func.any_(["%" + keyword + "%"])
        )
    ).all()
    return insts


def list_by_user_id(user_id):
    """Returns all Institutions by user id"""
    insts = InstitutionModel.query.filter(
        InstitutionModel.id.in_(
            InstitutionUserRoleModel.query.with_entities(
                InstitutionUserRoleModel.institution_id
            ).filter_by(user_id=user_id)
        )
    ).all()
    return insts


def create_new(
    name, address, location, web, keywords, days_and_opening_hours, email, information
):
    """Create a new institution"""
    try:
        institution = InstitutionModel(
            name=name,
            address=address,
            location=location,
            web=web,
            keywords=keywords,
            days_and_opening_hours=days_and_opening_hours,
            email=email,
            information=information,
            enabled=True,
        )

        db.session.add(institution)
        db.session.commit()
    except SQLAlchemyError as exc:
        db.session.rollback()
        raise exceptions.BadRequest(
            "El nombre de institucion o email ya existe"
        ) from exc
    return institution


def get_by_user_id(user_id):
    """Returns an institution by user id"""
    inst_user_role = InstitutionUserRoleModel.query.filter_by(user_id=user_id).first()
    if inst_user_role is None:
        return None
    institution = InstitutionModel.query.filter_by(
        id=inst_user_role.institution_id
    ).first()
    return institution


def get_by_id(inst_id):
    """Returns an institution by id"""
    institution = InstitutionModel.query.filter_by(id=inst_id).first()
    return institution


def get_by_name(inst_name):
    """Returns an institution by name"""
    institution = InstitutionModel.query.filter_by(name=inst_name).first()
    return institution


def get_by_email(instemail):
    """Returns an institution searching by email"""
    institution = InstitutionModel.query.filter_by(email=instemail).first()
    return institution


def delete(institution):
    """Deletes an institution"""
    db.session.delete(institution)
    db.session.commit()
    return institution


def update(institution, data):
    """Updates an institution"""
    for key, item in data.items():
        setattr(institution, key, item)

    db.session.commit()
    return institution


def rank_by_time_resolution():
    """Returns the institutions ordered by time resolution(time since a request is created until it is finished)."""
    # This query is right, by i also need to add the time resolution in the response
    institutions = (
        InstitutionModel.query.join(ServiceModel)
        .join(ServiceRequestModel)
        .with_entities(
            InstitutionModel.id,
            InstitutionModel.name,
            InstitutionModel.email,
            InstitutionModel.address,
            InstitutionModel.location,
            InstitutionModel.enabled,
            func.avg(
                ServiceRequestModel.close_date - ServiceRequestModel.creation_date
            ).label("time_resolution"),
        )
        .group_by(InstitutionModel.id)
        .order_by("time_resolution")
        .all()
    )

    return institutions
