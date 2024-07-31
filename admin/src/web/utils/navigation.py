from flask import session, url_for

from src.dbo import inst_user_role_dbo, role_dbo
from src.models.enums import Roles
from src.web.utils import auth
from src.web.utils import session as session_utils


def get_menu():
    """Returns the menu items."""
    menu = []
    if not auth.is_logged_in():
        menu = [
            {"label": "Iniciar Sesión", "url": url_for("auth.login_page")},
            {"label": "Registrar Usaurio", "url": url_for("auth.register_page")},
        ]
    else:
        session_id = session_utils.get_user_id()
        inst_id = session_utils.get_inst_id()

        if inst_id is not None:
            role = inst_user_role_dbo.get_role(session_id, inst_id)
            menu = [
                {"label": "Inicio", "url": url_for("home.home_page")},
                {
                    "label": "Gestion de Solicitudes",
                    "url": url_for("service_request.service_request_index"),
                },
                {
                    "label": "Administracion de Servicios",
                    "url": url_for("services.service_index"),
                },
            ]
            if role == Roles.OWNER.value:
                menu.append(
                    {
                        "label": "Administracion de Usuarios",
                        "url": url_for("inst_user_role.institution_users_page"),
                    }
                )
        else:
            role = role_dbo.get_role(session_id)
            if role == Roles.SUPERADMIN.value:
                menu = [
                    {"label": "Inicio", "url": url_for("home.home_page")},
                    {
                        "label": "Administracion de Usuarios",
                        "url": url_for("users.user_index"),
                    },
                    {
                        "label": "Administracion de Instituciones",
                        "url": url_for("institutions.institution_index"),
                    },
                    {
                        "label": "Configuracion de la Aplicacion",
                        "url": url_for("configuration.configuration_page"),
                    },
                ]

    return menu
