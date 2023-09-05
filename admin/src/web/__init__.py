from flask import Flask
from flask import render_template

def create_app(env="development", static_folder="./static"):
    """"Create app docstring"""
    app = Flask(__name__, static_folder=static_folder)

    @app.get("/")
    def home():
        return render_template("home.html")
    
    return app