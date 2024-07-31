from src.core.database import HelperModel, db


class SimpleUserModel(db.Model, HelperModel):
    """Temporal user model"""

    __tablename__ = "simple-user"

    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    email = db.Column(db.String(), unique=True)

    def __init__(self, firstname, lastname, email):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
