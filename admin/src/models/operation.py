from src.core.database import db


class OperationModel(db.Model):
    """Main user model"""

    __tablename__ = "operation"

    id = db.Column(db.Integer(), primary_key=True)
    operation = db.Column(db.String(), unique=True, nullable=False)

    def __init__(self, operation):
        self.operation = operation

    def __repr__(self):
        return f"<operation {self.operation}>"
