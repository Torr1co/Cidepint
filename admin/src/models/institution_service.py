from src.core.database import db


class InstitutionServiceModel(db.Model):
    """Main Institution Service model"""

    __tablename__ = "institution_service"
    __table_args__ = (
        db.UniqueConstraint(
            "institution_id", "service_id", name="unique_institution_service"
        ),
    )
    id = db.Column(db.Integer(), primary_key=True)
    institution_id = db.Column(db.Integer(), db.ForeignKey("institution.id"))
    service_id = db.Column(db.Integer(), db.ForeignKey("service.id"))

    def __init__(self, service_id, institution_id):
        self.service_id = service_id
        self.institution_id = institution_id

    def __repr__(self):
        return f"<permission {self.permission}>"
