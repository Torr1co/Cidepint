"""Auth routing logic"""
from flask import (
    Blueprint,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.exceptions import HTTPException, Unauthorized

from src.dbo import institution_dbo, role_dbo, simple_user_dbo, user_dbo
from src.web.utils import session as session_utils
from src.web.utils.api import error_response, response_handler
from src.web.utils.auth import is_logged_in
from src.web.utils.forms.auth import LoginForm, RegisterForm
from src.web.utils.jwt import jwt_auth
from src.web.utils.oauth import oauth

auth_routing = Blueprint(
    "auth",
    __name__,
    static_folder="static",
    template_folder="templates",
    url_prefix="/auth",
)


@auth_routing.route("/login/google")
def google_login():
    """logins with google"""
    return oauth.google.authorize_redirect(
        url_for("auth.google_callback", _external=True)
    )


@auth_routing.route("/login/callback")
def google_callback():
    token = oauth.google.authorize_access_token()

    if token is None:
        flash("Parametros invalidos", "error")
    else:
        me = token["userinfo"]
        user = user_dbo.get_by_email(me["email"])
        if user is None:
            user = simple_user_dbo.get_by_email(me["email"])
            if user is None:
                user = simple_user_dbo.create_new(
                    firstname=me["given_name"],
                    lastname=me["family_name"],
                    email=me["email"],
                )
            return redirect(url_for("users.confirm_user", user_id=user.id))
        auth = handle_auth(user)
        if auth.status_code != 200:
            flash(auth.json["error"], "error")

    return redirect(url_for("auth.login_page"))


@auth_routing.route("/login", methods=["GET", "POST"])
def login_page():
    """Returns the login page"""
    if request.method == "POST":
        form = LoginForm(request.form)
        user = user_dbo.get_by_email(form.email.data)
        if not user or not user.check_password(form.password.data):
            flash("Parametros invalidos", "error")
        auth = handle_auth(user)
        if auth.status_code != 200:
            flash(auth.json["error"], "error")
        return redirect(url_for("auth.login_page"))

    if is_logged_in():
        return redirect(url_for("home.home_page"))
    return render_template("login.html", form=LoginForm())


@auth_routing.post("/logout")
def logout():
    """Returns the login page and closes the session"""
    if is_logged_in():
        session.clear()
        response_handler(
            make_response(
                jsonify({"message": "Sesión cerrada exitosamente!"}),
                200,
            )
        )
    else:
        response_handler(error_response(Unauthorized("No se encuentra logueado")))
    return redirect(url_for("auth.login_page"))


@auth_routing.route("/register", methods=["GET"])
def register_page():
    """Returns the register page"""
    if is_logged_in():
        return redirect(url_for("home.home_page"))
    return render_template("register.html", form=RegisterForm())


@auth_routing.post("/")
def handle_auth(user):
    """
    Authenticates the user and returns a JWT token
    """

    try:
        insts = institution_dbo.list_by_user_id(user.id)
        role = role_dbo.get_role(user.id)

        if not user.active or (not role and len(insts) == 0):
            raise Unauthorized("No tiene permisos para acceder a la aplicación")

        token = jwt_auth.encode({"user_id": user.id})
        session["jwt_token"] = token

        if len(insts) > 0:
            session_utils.set_institutions(insts)
        else:
            session["role"] = role

        return make_response(
            jsonify({"token": token}),
            200,
            {"WWW-Authenticate": 'Basic realm="Authentication Successful"'},
        )
    except HTTPException as e:
        return error_response(e)
