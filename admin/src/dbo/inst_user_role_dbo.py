from src.core.database import db
from src.dbo import user_dbo
from src.models.enums import Roles
from src.models.institution_user_role import InstitutionUserRoleModel


def search(inst_id, page, per_page):
    """Searches for the users from an especific institution"""
    institution_user_roles = InstitutionUserRoleModel.query.filter(
        InstitutionUserRoleModel.institution_id == inst_id,
        InstitutionUserRoleModel.role != Roles.OWNER.value,
    ).paginate(page=page, per_page=per_page, error_out=False)

    results = []
    for iur in institution_user_roles:
        user = user_dbo.get_by_id(iur.user_id)
        result_item = {
            **user.serialize(),
            "role": iur.role,
            "institution_id": iur.institution_id,
        }

        results.append(result_item)

    return results, institution_user_roles.pages


def create_new(institution_id, user_email, role):
    """Creates a new user role for an institution"""
    user = user_dbo.get_by_email(user_email)
    if not user:
        return None

    new_institution_user_role = InstitutionUserRoleModel(
        user_id=user.id, role=role, institution_id=institution_id
    )
    db.session.add(new_institution_user_role)
    db.session.commit()
    return new_institution_user_role


def get_role(user_id, institution_id):
    """Gets the role of a user in an institution"""

    inst_user_role = InstitutionUserRoleModel.query.filter_by(
        user_id=user_id, institution_id=institution_id
    ).first()

    if not inst_user_role:
        return None

    return inst_user_role.role


def update_role(user_id, institution_id, role):
    """Updates the role of a user in an institution"""

    inst_user_role = InstitutionUserRoleModel.query.filter_by(
        user_id=user_id, institution_id=institution_id
    ).first()

    inst_user_role.role = role
    db.session.commit()
    return inst_user_role


def delete_role(user_id, institution_id):
    """Deletes the role of a user in an institution"""

    inst_user_role = InstitutionUserRoleModel.query.filter_by(
        user_id=user_id, institution_id=institution_id
    ).first()

    db.session.delete(inst_user_role)
    db.session.commit()
    return inst_user_role
