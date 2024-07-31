from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField
from wtforms.validators import DataRequired, Length, Regexp

from src.web.utils.forms.choices import service_lab_choices


class ServiceCreateForm(FlaskForm):
    name = StringField("Nombre", validators=[DataRequired("Campo requerido")])
    description = StringField(
        "Descripción", validators=[DataRequired("Campo requerido")]
    )
    keywords = StringField(
        "Palabras clave",
        validators=[
            DataRequired("Campo requerido"),
            Length(max=100, message="Máximo 100 caracteres"),
            Regexp(
                r"^([a-zA-Z0-9]+)(,\s*[a-zA-Z0-9]+)*$",
                message="Solo letras y números separados por coma",
            ),
        ],
    )
    service_type = StringField(
        "Tipo de Servicio", validators=[DataRequired("Campo requerido")]
    )
    service_type = SelectField("Tipo de servicio", choices=service_lab_choices)


class ServiceUpdateForm(ServiceCreateForm):
    enabled = BooleanField("Habilitado", validators=[DataRequired("Campo requerido")])
