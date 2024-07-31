from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms.validators import DataRequired


class ConfirmDeleteForm(FlaskForm):
    confirm = BooleanField("", validators=[DataRequired("Campo requerido")])
