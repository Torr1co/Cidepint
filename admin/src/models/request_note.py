"""Institution model"""
from src.core.database import HelperModel, db


class RequestNoteModel(db.Model, HelperModel):
    """Main request note model"""

    __tablename__ = "service_request_note"

    id = db.Column(db.Integer(), primary_key=True)
    note = db.Column(db.String())
    creation_date = db.Column(db.DateTime())
    service_request_id = db.Column(db.Integer(), db.ForeignKey("service_request.id"))
    author_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

    def __init__(self, note, service_request_id, author_id):
        self.note = note
        self.service_request_id = service_request_id
        self.author_id = author_id
