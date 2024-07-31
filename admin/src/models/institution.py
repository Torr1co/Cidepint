"""Institution model"""
from src.core.database import HelperModel, db


class InstitutionModel(db.Model, HelperModel):
    """Main Institution model"""

    __tablename__ = "institution"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)
    information = db.Column(db.String())
    address = db.Column(db.String())
    location = db.Column(db.String())
    web = db.Column(db.String())
    days_and_opening_hours = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    enabled = db.Column(db.Boolean(), default=True)
    keywords = db.Column(db.ARRAY(db.String()))

    def __init__(
        self,
        name,
        address,
        location,
        web,
        keywords,
        days_and_opening_hours,
        email,
        information,
        enabled=False,
    ):
        self.name = name
        self.address = address
        self.location = location
        self.web = web
        self.keywords = keywords
        self.days_and_opening_hours = days_and_opening_hours
        self.email = email
        self.information = information
        self.enabled = enabled
