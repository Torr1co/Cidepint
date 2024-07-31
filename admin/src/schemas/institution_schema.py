from marshmallow import Schema, fields, validate


class InstitutionSchema(Schema):
    """general ïnstitution schema"""

    id = fields.Integer()
    name = fields.Str(
        required=True,
        validate=(validate.Length(max=100), validate.Regexp(r"^[a-zA-Z0-9 ]$")),
    )
    information = fields.Str(required=True, validate=validate.Length(max=1000))
    address = fields.Str(required=True, validate=validate.Length(max=100))
    location = fields.String(required=True, validate=validate.Length(max=100))
    web = fields.Str(required=True, validate=validate.Length(max=100))
    days_and_opening_hours = fields.Str(
        required=True, validate=validate.Length(max=100)
    )
    email = fields.Email(required=True, validate=validate.Length(max=100))
    enabled = fields.Boolean()
    keywords = fields.List(
        fields.String(validate=validate.Regexp(r"^[a-zA-Z0-9]+$")),
    )


class InstitutionAnalisisSchema(InstitutionSchema):
    """institution schema for analisis"""

    time_resolution = fields.TimeDelta(precision="seconds")


institution_schema = InstitutionSchema()
many_institution_schema = InstitutionSchema(exclude=("keywords", "id"), many=True)
index_institution_schema = InstitutionSchema(
    only=("id", "name", "email", "address", "location", "enabled"), many=True
)
institution_analisis_schema = InstitutionAnalisisSchema(many=True)
