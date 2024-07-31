from marshmallow import Schema, ValidationError, fields, validate, validates

from src.models.enums import UserDocument, UserGender


class GetUserSchema(Schema):
    """
    Response Body:{
        "user": "usarname",
        "email": "username@mail.com",
        "document_type": "DNI",
        "document_number": "35.555.555",
        "gender": "Masculino",
        "gender_other": "transgénero",
        "address": "120 y 50",
        "phone": "221 1212-123"
    }

    """

    id = fields.Int()
    firstname = fields.Str(validate=validate.Length(max=50), required=True)
    lastname = fields.Str(validate=validate.Length(max=50), required=True)
    user = fields.Str(validate=validate.Length(max=50), required=True)
    email = fields.Email(validate=validate.Email())
    active = fields.Bool()
    document_type = fields.Enum(UserDocument)
    document_number = fields.Str(validate=validate.Length(max=10), required=True)
    gender = fields.Enum(UserGender)
    gender_other = fields.Str(validate=validate.Length(max=20))
    address = fields.Str(validate=validate.Length(max=50), required=True)
    phone = fields.Str(validate=validate.Length(max=50), required=True)


get_user_schema = GetUserSchema(
    only=(
        "email",
        "document_type",
        "document_number",
        "gender",
        "gender_other",
        "address",
        "phone",
    )
)
