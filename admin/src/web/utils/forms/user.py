from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, StringField
from wtforms.validators import DataRequired, Length, Regexp

from src.models.enums import UserDocument, UserGender

document_type_choices = [
    (UserDocument.DNI.name, UserDocument.DNI.value),
    (UserDocument.CIVIC.name, UserDocument.CIVIC.value),
    (UserDocument.ENROLMENT.name, UserDocument.ENROLMENT.value),
]

user_gender_choices = [
    (UserGender.MALE.name, UserGender.MALE.value),
    (UserGender.FEMALE.name, UserGender.FEMALE.value),
    (UserGender.OTHER.name, UserGender.OTHER.value),
    (UserGender.NOT_SPECIFIED.name, UserGender.NOT_SPECIFIED.value),
]


class UserUpdateForm(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(),
            Length(max=100, message="Máximo 100 caracteres"),
            Regexp(r"^[a-zA-Z0-9 ]*$", message="Solo letras y números"),
        ],
    )
    firstname = StringField("Nombre", validators=[DataRequired()])
    lastname = StringField("Apellido", validators=[DataRequired()])
    document_type = SelectField("Tipo de documento", choices=document_type_choices)
    document_number = StringField("Número de documento")
    gender = SelectField("Genero", choices=user_gender_choices)
    gender_other = StringField(
        "Otro genero",
        render_kw={"class": "hidden"},
    )
    address = StringField("Dirección")
    phone = StringField("Teléfono")
    active = BooleanField("Habilitado")
