from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp


class InstitutionCreateForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(max=100, message="Máximo 100 caracteres"),
            Regexp(r"^[a-zA-Z0-9 ]*$", message="Solo letras y números"),
        ],
    )
    address = StringField(
        "Dirección",
        validators=[DataRequired(), Length(max=100, message="Máximo 100 caracteres")],
    )
    location = StringField(
        "Localización",
        validators=[DataRequired(), Length(max=100, message="Máximo 100 caracteres")],
    )
    web = StringField(
        "Web",
        validators=[DataRequired(), Length(max=100, message="Máximo 100 caracteres")],
    )
    days_and_opening_hours = StringField(
        "Cronograma",
        validators=[DataRequired(), Length(max=100, message="Máximo 100 caracteres")],
    )
    information = TextAreaField(
        "Información",
        validators=[DataRequired(), Length(max=1000, message="Máximo 1000 caracteres")],
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
    email = EmailField(
        "Correo",
        validators=[
            Email("Correo invalido"),
            DataRequired(),
            Length(max=100, message="Máximo 100 caracteres"),
        ],
    )


class InstitutionUpdateForm(InstitutionCreateForm):
    enabled = BooleanField("Habilitado")


class InstitutionAddOwnerForm(FlaskForm):
    email = EmailField("Correo", validators=[Email("Correo invalido")])
