from src.core.database import db
from src.models.enums import Operations
from src.models.operation import OperationModel


def crud_operations(operation_name, exclude=None):
    """
    Creates the CRUD operations for the given name.
    index, create, delete, update, show
    """
    if exclude is None:
        exclude = []
    operations = []
    if "index" not in exclude:
        operations.append(f"{operation_name}_index")
    if "create" not in exclude:
        operations.append(f"{operation_name}_create")
    if "delete" not in exclude:
        operations.append(f"{operation_name}_delete")
    if "update" not in exclude:
        operations.append(f"{operation_name}_update")
    if "show" not in exclude:
        operations.append(f"{operation_name}_show")

    return operations


def create_operations():
    """
    Creates the operations for the app.
    """
    operations = [
        *crud_operations(Operations.USER.value),
        *crud_operations(Operations.INSTITUTION.value),
        *crud_operations(Operations.INSTITUTION_USER.value),
        *crud_operations(Operations.SERVICE.value),
        *crud_operations(Operations.SERVICE_REQUEST.value, exclude=["create"]),
        Operations.CONFIG.show,
        Operations.CONFIG.update,
    ]
    for operation in operations:
        new_operation = OperationModel(operation)
        db.session.add(new_operation)
        db.session.commit()
