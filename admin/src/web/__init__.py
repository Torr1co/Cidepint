from flask import Flask

def create_app():
    """"Create app docstring"""
    app = Flask(__name__)

    @app.get("/")
    def home():
        return "Hola munsdoaawsdasd"
    
    return app