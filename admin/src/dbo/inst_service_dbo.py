from models.institution_service import InstitutionServiceModel
from src.core.database import db


def create_new(service_id, institution_id):
    """Creates a new user role for an institution"""

    new_institution_service = InstitutionServiceModel(
        service_id=service_id, institution_id=institution_id
    )
    db.session.add(new_institution_service)
    db.session.commit()
    return new_institution_service
