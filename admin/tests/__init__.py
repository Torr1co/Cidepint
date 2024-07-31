from src.web import create_app

app = create_app(env="testing")
client = app.test_client()
