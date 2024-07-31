from src.core.database import db


class PermissionModel(db.Model):
    """Main user model"""

    __tablename__ = "permission"

    id = db.Column(db.Integer(), primary_key=True)
    operation = db.Column(db.String(), db.ForeignKey("operation.operation"))
    role = db.Column(db.String(), db.ForeignKey("role.role"))

    def __init__(self, role, operation):
        self.role = role
        self.operation = operation

    def __repr__(self):
        return f"<permission {self.permission}>"
