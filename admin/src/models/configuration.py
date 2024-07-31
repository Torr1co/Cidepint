"""Configuration model"""
from src.core.database import HelperModel, db


class ConfigurationModel(db.Model, HelperModel):
    """Configuration model"""

    __tablename__ = "configuration"

    id = db.Column(db.Integer(), primary_key=True)
    elements_per_page = db.Column(db.Integer)
    phone_number = db.Column(db.String())
    email = db.Column(db.String())
    maintenance_mode = db.Column(db.Boolean(), default=False)
    maintenance_message = db.Column(db.String())

    def __init__(
        self,
        elements_per_page,
        phone_number,
        email,
        maintenance_mode=False,
        maintenance_message=None,
    ):
        self.elements_per_page = elements_per_page
        self.phone_number = phone_number
        self.email = email
        self.maintenance_mode = maintenance_mode
        self.maintenance_message = maintenance_message

    @classmethod
    def get_singleton(cls):
        return cls.query.first()

    @classmethod
    def get_elements_per_page(self):
        return self.elements_per_page

    @classmethod
    def get_phone_number(self):
        return self.phone_number

    @classmethod
    def get_email(self):
        return self.email

    @classmethod
    def get_maintenance_mode(self):
        return self.maintenance_mode

    def get_maintenance_message(self):
        return self.maintenance_message
