from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, Length, Regexp


class LoginForm(FlaskForm):
    """Main Login Form Model"""

    email = EmailField("Correo", validators=[Email()])
    password = PasswordField("Contraseña", validators=[DataRequired("Campo requerido")])


class RegisterForm(FlaskForm):
    """Main Register Form Model"""

    email = EmailField("Correo", validators=[Email()])
    firstname = StringField("Nombre", validators=[DataRequired("Campo requerido")])
    lastname = StringField("Apellido", validators=[DataRequired("Campo requerido")])


class ConfirmRegisterForm(FlaskForm):
    """Confirm Register Form Model"""

    username = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(),
            Length(max=100, message="Máximo 100 caracteres"),
            Regexp(r"^[a-zA-Z0-9 ]*$", message="Solo letras y números"),
        ],
    )
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=8)])
