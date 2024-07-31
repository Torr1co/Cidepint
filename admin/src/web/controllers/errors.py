"""error routing and utils"""
from flask import Blueprint, abort, render_template

from src.dbo import configuration_dbo

error_routing = Blueprint(
    "errors",
    __name__,
    static_folder="static",
    template_folder="templates",
)


# Error pages
@error_routing.get("/401")
def error_401():
    """Defines the 401 error page"""
    abort(401)


@error_routing.get("/403")
def error_403():
    """Defines the 403 error page"""
    abort(403)


@error_routing.get("/404")
def error_404():
    """Defines the 404 error page"""
    abort(404)


@error_routing.get("/500")
def error_500():
    """Defines the 500 error page"""
    abort(500)


@error_routing.get("/503")
def error_503():
    """Defines the 503 error page"""
    abort(503)


# Error handlers
@error_routing.app_errorhandler(401)
def unauthorized(_error):
    """Returns the 401 error page"""
    return render_template("errors/401.html"), 401


@error_routing.app_errorhandler(403)
def forbidden(_error):
    """Returns the 403 error page"""
    return render_template("errors/403.html"), 403


@error_routing.app_errorhandler(404)
def page_not_found(_error):
    """Returns the 404 error page"""
    return render_template("errors/404.html"), 404


@error_routing.app_errorhandler(500)
def internal_server_error(_error):
    """Returns the 500 error page"""
    return render_template("errors/500.html"), 500


@error_routing.app_errorhandler(503)
def service_unavailable(_error):
    """Returns the 503 error page"""
    config = configuration_dbo.get_configuration()
    return render_template("errors/503.html", config=config), 503
