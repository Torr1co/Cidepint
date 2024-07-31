from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired

from src.models.enums import ServiceRequestStatus
from src.web.utils.forms.choices import service_lab_choices

request_choices = [(status.name, status.value) for status in ServiceRequestStatus]


class ServiceRequestSearchForm(FlaskForm):
    user_id = SelectField("Usuario")
    service_type = SelectField(
        "Tipo de servicio", choices=[("", "Todos"), *service_lab_choices]
    )
    status = SelectField("Estado", choices=[("", "Todos"), *request_choices])
    creation_date_start = DateField("Fecha de creación desde")
    creation_date_end = DateField("Fecha de creación hasta")


class ServiceRequestCreateForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired("Campo requerido")])
    description = TextAreaField(
        "Descripción", validators=[DataRequired("Campo requerido")]
    )
    status = SelectField(
        "Estado", choices=request_choices, validators=[DataRequired("Campo requerido")]
    )
    service_id = StringField("Servicio", validators=[DataRequired("Campo requerido")])


class ServiceRequestUpdateForm(FlaskForm):
    status = SelectField(
        "Estado", choices=request_choices, validators=[DataRequired("Campo requerido")]
    )


class ServiceRequestNoteForm(FlaskForm):
    note = TextAreaField("Comentario", validators=[DataRequired("Campo requerido")])
