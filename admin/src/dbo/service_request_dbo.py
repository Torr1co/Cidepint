from datetime import datetime

from sqlalchemy import and_, or_

from src.core.database import db
from src.models.enums import ServiceRequestStatus
from src.models.request_note import RequestNoteModel
from src.models.service import ServiceModel
from src.models.service_request import ServiceRequestModel
from src.models.user import UserModel


def search(user_id, page, per_page):
    """Returns all ServiceRequests by search params"""
    return ServiceRequestModel.query.filter_by(user_id=user_id).paginate(
        page=page, per_page=per_page, error_out=False
    )


def search_by_user(
    inst_id,
    user_id,
    creation_date_start,
    creation_date_end,
    service_type,
    status,
    page,
    per_page,
):
    """Returns filtered ServiceRequests by search params"""
    service_requests = ServiceRequestModel.query.filter(
        ServiceRequestModel.user_id == user_id if user_id else True,
        ServiceRequestModel.creation_date.between(
            [creation_date_start, creation_date_end]
        )
        if creation_date_start and creation_date_end
        else True,
        ServiceRequestModel.status == status if status else True,
        ServiceRequestModel.service_id == ServiceModel.id,
        ServiceModel.institution_id == inst_id,
        ServiceModel.service_type == service_type if service_type else True,
    ).paginate(page=page, per_page=per_page, error_out=False)

    results = []
    for request in service_requests.items:
        user = UserModel.query.get(request.user_id)
        service = ServiceModel.query.get(request.service_id)
        result_item = {
            **request.serialize(),
            "user": user.serialize(),
            "service": service.serialize(),
        }
        results.append(result_item)
    return results, service_requests.pages


def get_by_id(request_id):
    """Returns a ServiceRequest by id"""
    return ServiceRequestModel.query.filter_by(id=request_id).first()


def get_related_by_id(request_id):
    """Returns related information of a ServiceRequest by id"""
    request = ServiceRequestModel.query.filter_by(id=request_id).first()
    user = UserModel.query.get(request.user_id)
    service = ServiceModel.query.get(request.service_id)
    result = {
        **request.serialize(),
        "user": user.serialize(),
        "service": service.serialize(),
    }
    return result


def update(request_id, status):
    """Updates a ServiceRequest"""
    service_request = ServiceRequestModel.query.filter_by(id=request_id).first()
    service_request.status = status
    if status == ServiceRequestStatus.FINISHED.name and not service_request.close_date:
        service_request.close_date = datetime.now()
    else:
        service_request.close_date = None
    db.session.commit()
    return service_request


def create_new(title, description, user_id, service_id, status):
    """Creates a new ServiceRequest"""
    service_request = ServiceRequestModel(
        title=title,
        description=description,
        status=status,
        user_id=user_id,
        service_id=service_id,
    )
    db.session.add(service_request)
    db.session.commit()
    return service_request


def add_note(req_id, author_id, note):
    """Adds a new note to a ServiceRequest"""
    request_note = RequestNoteModel(
        note=note,
        author_id=author_id,
        service_request_id=req_id,
    )
    db.session.add(request_note)
    db.session.commit()
    return request_note


def get_notes_by_req(req_id):
    """Returns all notes from a ServiceRequest"""
    notes = RequestNoteModel.query.filter_by(service_request_id=req_id).all()
    result = []
    for note in notes:
        author = UserModel.query.get(note.author_id)
        result.append({**note.serialize(), "author": author.serialize()})

    return result


def get_notes_by_user(user_id):
    """Returns all notes from a user"""
    notes = RequestNoteModel.query.filter_by(author_id=user_id).all()
    result = []
    for note in notes:
        author = UserModel.query.get(note.author_id)
        result.append({**note.serialize(), "author": author.serialize()})

    return result
