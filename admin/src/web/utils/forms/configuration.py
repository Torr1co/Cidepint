import re

from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, StringField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError


def validate_elements_per_page(form, field):
    """Validates the amount of elements per page"""

    try:
        float(field.data)
        if float(field.data) <= 0:
            raise ValidationError("Debe ingresar un número mayor a 0.")
    except ValueError:
        raise ValidationError("Debe ingresar un número mayor a 0.")


def validate_phone_number(form, field):
    """Validates the format of the phone number"""

    if not re.match(r"^\d+$", field.data):
        raise ValidationError(
            "Debe ingresar un número de teléfono válido (solo números)."
        )


class ConfigurationUpdateForm(FlaskForm):
    elements_per_page = StringField(
        "Elementos por página",
        validators=[DataRequired("Campo requerido"), validate_elements_per_page],
    )
    phone_number = StringField(
        "Número de teléfono de contacto",
        validators=[
            DataRequired("Campo requerido"),
            Length(min=1, message="Debe ingresar un número de teléfono."),
            validate_phone_number,
        ],
    )
    email = StringField(
        "Correo electrónico de contacto",
        validators=[
            DataRequired("Campo requerido"),
            Email(message="Debe ingresar un correo electrónico válido"),
        ],
    )
    maintenance_mode = BooleanField("Modo de mantenimiento")
    maintenance_message = StringField("Mensaje de mantenimiento")
