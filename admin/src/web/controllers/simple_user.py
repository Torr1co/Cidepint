"""User routing logic"""
from flask import Blueprint, current_app, flash, redirect, request, url_for
from flask_mail import Message
from werkzeug import exceptions

from src.core.email import mail
from src.dbo import simple_user_dbo

simpleuser_routing = Blueprint(
    "simpleusers",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/simpleusers",
)


def send_email(message):
    """
    Sends an email to the user with the received message as body
    :param message: message to be sent
    """
    msg = Message(
        subject=(
            f"{current_app.config['MAIL_USERNAME']} quiere contactarse contigo desde tu app"
        ),
        sender=current_app.config["MAIL_USERNAME"],
        recipients=[message.get("Email")],
        body=message.get("Message"),
    )
    mail.send(msg)


@simpleuser_routing.post("/")
def create_simpleuser():
    """
    Creates a new temp simpleuser (performs a simple registration)
    """
    try:
        simpleuser = simple_user_dbo.create_new(
            firstname=request.form["firstname"],
            lastname=request.form["lastname"],
            email=request.form["email"],
        )
        # Sending email to the user
        message = {
            "Email": request.form["email"],
            "Message": f"Se ha recibido una solicitud de registro de tu dirección de correo al sitio WEB Admin CIDEPINT.\nPara completaria entra al link: {request.url_root}users/confirm/{simpleuser.id}",  # Here we should send the link to /users/confirm/<userid> no matter the enviroment
        }
        send_email(message=message)
        flash("Se ha enviado un correo de confirmación a su dirección", "success")
    except exceptions.HTTPException as e:
        flash(e.description, "error")
        return redirect(url_for("auth.register_page"))
    return redirect(url_for("auth.login_page"))
