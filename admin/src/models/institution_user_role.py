from src.core.database import db


class InstitutionUserRoleModel(db.Model):
    """inst_user_role relation"""

    __tablename__ = "institution_user_role"
    __table_args__ = (
        db.UniqueConstraint("user_id", "institution_id", name="unique_inst_user_role"),
    )
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id", ondelete="CASCADE"))
    role = db.Column(db.String(), db.ForeignKey("role.role", ondelete="CASCADE"))
    institution_id = db.Column(
        db.Integer(), db.ForeignKey("institution.id", ondelete="CASCADE")
    )

    def __init__(self, user_id, institution_id, role):
        self.user_id = user_id
        self.institution_id = institution_id
        self.role = role

    def __repr__(self):
        return f"<permission {self.user_id}>"
