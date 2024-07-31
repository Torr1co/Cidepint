from src.core.database import db
from src.dbo.operation_dbo import crud_operations
from src.models.enums import Roles
from src.models.permission import PermissionModel

permissions = {
    Roles.OWNER.value: [
        "institution_user_create",
        "institution_user_delete",
        *crud_operations("institution_user", exclude=["show"]),
        *crud_operations("service"),
        *crud_operations("service_request", exclude=["create"]),
    ],
    Roles.ADMINISTRATOR.value: [
        *crud_operations("service"),
        *crud_operations("service_request", exclude=["create"]),
    ],
    Roles.OPERATOR.value: [
        *crud_operations("service", exclude=["delete"]),
        *crud_operations("service_request", exclude=["create", "delete"]),
    ],
    Roles.SUPERADMIN.value: [
        *crud_operations("user"),
        *crud_operations("institution"),
        "institution_user_create",
        "config_show",
        "config_update",
    ],
}


def create_permissions():
    """
    Creates the permissions for the app.
    """
    for role, operations in permissions.items():
        for operation in operations:
            new_permission = PermissionModel(role=role, operation=operation)
            db.session.add(new_permission)
            db.session.commit()


def check_permission(role, operation):
    """
    Gets the operation by role and operation.
    """
    return (
        PermissionModel.query.filter_by(role=role, operation=operation).first()
        is not None
    )
