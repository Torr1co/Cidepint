from flask_wtf import FlaskForm
from wtforms import EmailField, SelectField
from wtforms.validators import Email

from src.models.enums import Roles

roles_choices = [
    (Roles.ADMINISTRATOR.value, "Administrador"),
    (Roles.OPERATOR.value, "Operador"),
]


class UserUpdateInstRoleForm(FlaskForm):
    role = SelectField("Rol", choices=roles_choices)


class InstitutionAddUserForm(FlaskForm):
    email = EmailField("Correo", validators=[Email("Correo invalido")])
    role = SelectField("Rol", choices=roles_choices)
