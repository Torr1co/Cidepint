"""home routing logic"""
from flask import Blueprint, redirect, render_template, url_for

from src.web.utils.auth import is_logged_in

home_routing = Blueprint(
    "home",
    __name__,
    static_folder="static",
    template_folder="templates",
)


@home_routing.route("/", methods=["GET"])
def home_page():
    """Returns the home page"""
    if is_logged_in():
        return render_template("home.html")
    else:
        return redirect(url_for("auth.login_page"))
