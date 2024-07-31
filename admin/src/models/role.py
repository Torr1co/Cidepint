"""User model"""
from src.core.database import db


class RoleModel(db.Model):
    """Main role model"""

    __tablename__ = "role"

    id = db.Column(db.Integer(), primary_key=True)
    role = db.Column(db.String(), unique=True, nullable=False)

    def __init__(self, role):
        self.role = role

    def __repr__(self):
        return f"<Role {self.role}>"


class UserRoleModel(db.Model):
    # user role relationship

    __tablename__ = "user_role"
    __table_args__ = (db.UniqueConstraint("user_id", "role", name="unique_user_role"),)

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    role = db.Column(db.String(), db.ForeignKey("role.role"))

    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role = role

    def __repr__(self):
        return f"<AdminRole {self.user_id}>"
