from src.dbo import (
    inst_user_role_dbo,
    institution_dbo,
    role_dbo,
    service_dbo,
    service_request_dbo,
    user_dbo,
)
from src.dbo.operation_dbo import create_operations
from src.dbo.permission_dbo import create_permissions
from src.dbo.role_dbo import create_roles
from src.models.enums import Roles, ServiceRequestStatus, ServiceTypes


def create_mockup_info():
    """
    Creates a functional helper for testing purposes
    """
    superadmin = user_dbo.create_new(
        firstname="superadmin",
        lastname="Mock",
        username="superadmin",
        email="superadmin@email.com",
        password="superadmin",
    )
    owner = user_dbo.create_new(
        firstname="owner",
        lastname="Mock",
        username="owner",
        email="owner@email.com",
        password="owner",
    )

    admin = user_dbo.create_new(
        firstname="admin",
        lastname="Mock",
        username="admin",
        email="admin@email.com",
        password="admin",
    )

    operator = user_dbo.create_new(
        firstname="operator",
        lastname="Mock",
        username="operator",
        email="operator@email.com",
        password="operator",
    )

    # create_new(name, dir, location, web, keyword, days_and_opening_hours, email, info):
    inst1 = institution_dbo.create_new(
        name="Institución de prueba",
        address="Calle 123",
        location="location",
        web="www.institution.com",
        keywords="a,b,c",
        days_and_opening_hours="9:00-18:00",
        email="institution@email.com",
        information="informacion extra adicional",
    )

    inst2 = institution_dbo.create_new(
        name="Institución de prueba 2",
        address="Calle 1234",
        location="location2",
        web="www.institution2.com",
        keywords="a,b,c",
        days_and_opening_hours="9:00-18:00",
        email="institution2@email.com",
        information="informacion extra adicional2",
    )

    service = service_dbo.create_new(
        name="Servicio Test",
        inst_id=inst1.id,
        description="Descripcion random",
        keywords=["Servi"],
        service_type=ServiceTypes.ANALYSIS.name,
    )

    service2 = service_dbo.create_new(
        name="Servicio Test2222",
        inst_id=inst2.id,
        description="Descripcion random22",
        keywords=["Servi22"],
        service_type=ServiceTypes.CONSULTING.name,
    )

    role_dbo.create_new(user_id=superadmin.id, role=Roles.SUPERADMIN.value)

    inst_user_role_dbo.create_new(
        user_email=owner.email,
        role=Roles.OWNER.value,
        institution_id=inst1.id,
    )

    inst_user_role_dbo.create_new(
        user_email=admin.email, role=Roles.ADMINISTRATOR.value, institution_id=inst1.id
    )

    inst_user_role_dbo.create_new(
        user_email=operator.email, role=Roles.OPERATOR.value, institution_id=inst1.id
    )

    inst_user_role_dbo.create_new(
        user_email=operator.email, role=Roles.OPERATOR.value, institution_id=inst2.id
    )

    inst_user_role_dbo.create_new(
        user_email=admin.email, role=Roles.ADMINISTRATOR.value, institution_id=inst2.id
    )

    service_request_dbo.create_new(
        title="Solicitud de prueba",
        description="Descripcion de prueba",
        status=ServiceRequestStatus.PENDING.name,
        user_id=operator.id,
        service_id=service.id,
    )

    service_request_dbo.create_new(
        title="Solicitud de prueba2",
        description="Descripcion de prueba",
        status=ServiceRequestStatus.FINISHED.name,
        user_id=admin.id,
        service_id=service2.id,
    )

    service_request_dbo.create_new(
        title="Solicitud de prueba",
        description="Descripcion de prueba",
        status=ServiceRequestStatus.PENDING.name,
        user_id=operator.id,
        service_id=service2.id,
    )

    service_request_dbo.create_new(
        title="Solicitud de prueba2",
        description="Descripcion de prueba",
        status=ServiceRequestStatus.FINISHED.name,
        user_id=admin.id,
        service_id=service.id,
    )

    return {"status": "success"}


def seed_db():
    print("⚙️ Creating operations...")
    create_operations()
    print("⚙️ Creating roles...")
    create_roles()
    print("⚙️ Creating permissions...")
    create_permissions()
    print("⚙️ Creating mockup info...")
    create_mockup_info()
    print("✅ Database seeding Done!")
