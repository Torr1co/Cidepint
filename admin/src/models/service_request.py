"""Institution model"""
import datetime

from src.core.database import HelperModel, db
from src.models.enums import ServiceRequestStatus


class ServiceRequestModel(db.Model, HelperModel):
    """Main service request model"""

    __tablename__ = "service_request"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(511), nullable=False)
    status = db.Column(db.Enum(ServiceRequestStatus))
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"))
    service_id = db.Column(
        db.Integer(), db.ForeignKey("service.id", ondelete="CASCADE")
    )
    creation_date = db.Column(db.DateTime(), nullable=False)
    close_date = db.Column(db.DateTime(), nullable=True)

    def __init__(self, title, description, status, user_id, service_id):
        self.title = title
        self.description = description
        self.status = status
        self.user_id = user_id
        self.service_id = service_id
        self.creation_date = datetime.datetime.now()
