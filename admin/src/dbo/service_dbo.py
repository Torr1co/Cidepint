"""DBO for services model"""
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from werkzeug import exceptions

from src.core.database import db
from src.dbo import institution_dbo
from src.models.service import ServiceModel
from src.models.service_request import ServiceRequestModel
from src.web.utils import model as model_utils


def search_by_institution(inst_id, q, service_type, page, per_page):
    """
    Returns all services by the search param
    :param inst_id: institution id
    :param q: comma sepparated string with keywords to search
    :param service_type: service type
    :param page: page number
    :param per_page: page size
    """
    # TODO: Test this search function (including api usage)
    services = ServiceModel.query.filter(
        ServiceModel.institution_id == inst_id,
        func.array_to_string(ServiceModel.keywords, ",").ilike(
            func.any_(["%" + q + "%"])
        ),
        ServiceModel.service_type == service_type if service_type else True,
    ).paginate(page=page, per_page=per_page, error_out=False)

    results = []
    for service in services:
        inst = institution_dbo.get_by_id(service.institution_id)
        results.append(
            {
                **model_utils.enum_mutation(service.serialize(), lambda x: x.value),
                "laboratory": inst.name,
            }
        )

    return results, services.pages


def search(q, service_type, page=1, per_page=1):
    """
    Returns all services by the search param
    :param q: comma sepparated string with keywords to search
    :param service_type: service type
    :param inst_id: institution id
    :param page: page number
    :param per_page: page size
    """
    return ServiceModel.query.filter(
        func.array_to_string(ServiceModel.keywords, ",").ilike(
            func.any_(["%" + q + "%"])
        ),
        ServiceModel.service_type == service_type if service_type else True,
    ).paginate(page=page, per_page=per_page, error_out=False)


def list_all():
    """Returns all services"""
    services = ServiceModel.query.all()
    return services


def create_new(name, inst_id, description, keywords, service_type):
    """Creates a new service"""
    try:
        service = ServiceModel(
            name=name,
            inst_id=inst_id,
            description=description,
            keywords=keywords,
            service_type=service_type,
            enabled=True,
        )
        db.session.add(service)
        db.session.commit()
    except SQLAlchemyError as exc:
        db.session.rollback()
        raise exceptions.BadRequest("El nombre del servicio ya existe") from exc
    return service


def get_by_name(name):
    """Returns a service searching by name"""
    service = ServiceModel.query.filter_by(name=name).first()
    return service


def get_by_id(servid):
    """Returns a service searching by id"""
    service = ServiceModel.query.filter_by(id=servid).first()
    return service


def delete(service):
    """Deletes a service"""
    db.session.delete(service)
    db.session.commit()
    return service


def update(service, data):
    """Update a service"""
    service.name = data["name"]
    service.description = data["description"]
    service.keywords = data["keywords"]
    service.service_type = data["service_type"]
    service.enabled = data["enabled"]
    db.session.commit()
    return service


def get_types():
    """Returns all services types"""
    types = ServiceModel.query.with_entities(ServiceModel.service_type).distinct()
    return types


def search_types(inst_id, q):
    """Returns service types according to search param
    :param inst_id: institution id
    :param q: comma sepparated string with keywords to search
    """
    types = (
        ServiceModel.query.with_entities(ServiceModel.service_type)
        .filter(
            ServiceModel.institution_id == inst_id if inst_id else True,
            *(
                (
                    func.array_to_string(ServiceModel.keywords, ",").ilike(
                        func.any_(["%" + k + "%"])
                    )
                )
                for k in q.split(",")
            ),
        )
        .distinct()
    )
    return types


def rank_by_requests():
    """Returns the services ordered by requests."""
    services = (
        ServiceModel.query.join(ServiceRequestModel)
        .with_entities(
            ServiceModel.id,
            ServiceModel.name,
            ServiceModel.description,
            ServiceModel.keywords,
            ServiceModel.service_type,
            ServiceModel.enabled,
            func.count(ServiceRequestModel.id).label("request_count"),
        )
        .group_by(ServiceModel.id)
        .order_by(func.count(ServiceRequestModel.id).desc())
        .limit(10)
        .all()
    )
    return services


def requests_by_type():
    """Returns all service request grouped by service type"""
    types = (
        ServiceModel.query.join(ServiceRequestModel)
        .with_entities(
            ServiceModel.service_type,
            func.count(ServiceRequestModel.id).label("request_count"),
        )
        .group_by(ServiceModel.service_type)
        .all()
    )
    return types
