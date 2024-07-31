"""User model"""
from src.core.crypto import cipher
from src.core.database import HelperModel, db
from src.models.enums import UserDocument, UserGender


class UserModel(db.Model, HelperModel):
    """Main user model"""

    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String())
    lastname = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    username = db.Column(db.String(), unique=True, nullable=True)
    password = db.Column(db.String(), nullable=True)
    active = db.Column(db.Boolean(), default=False)
    document_type = db.Column(db.Enum(UserDocument), nullable=True)
    document_number = db.Column(db.String(), nullable=True)
    gender = db.Column(db.Enum(UserGender), nullable=True)
    gender_other = db.Column(db.String(), nullable=True)
    address = db.Column(db.String(), nullable=True)
    phone = db.Column(db.String(), nullable=True)

    def __init__(self, firstname, lastname, email, username, password, active=False):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password
        self.active = active

    def __repr__(self):
        return f"<User {self.username}>"

    def check_password(self, password):
        return (
            cipher.decrypt(bytes.fromhex(self.password.replace("\\x", ""))).decode(
                "utf-8"
            )
            == password
        )

    def serialize(self, exclude=[]):
        serialized = HelperModel.serialize(self, exclude)
        serialized.pop("password")
        return serialized
