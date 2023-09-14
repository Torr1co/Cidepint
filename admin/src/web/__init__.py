from flask import Flask
from flask import render_template

def create_app(env="development", static_folder="../../static"):
    """"Create app docstring"""
    app = Flask(__name__, static_folder=static_folder)

    @app.get("/")
    def home():
        return render_template("home.html")
    
    # Controladores para manejar errores
    @app.errorhandler(401)
    def unauthorized(error):
        return render_template("errors/401.html"), 401
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.html"), 500
    
    return app