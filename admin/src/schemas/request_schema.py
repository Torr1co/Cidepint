""" Esquema para la validación de los datos de entrada de los servicios."""
from marshmallow import Schema, fields, post_dump, validate

from src.models.enums import ServiceRequestStatus


class GetServiceSchema(Schema):
    """
    {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "name": {
        "type": "string",
        "description": "Nombre del servicio."
        },
        "description": {
        "type": "string",
        "description": "Descripción del servicio."
        },
        "laboratory": {
        "type": "string",
        "description": "Nombre del Laboratorio que presta el servicio."
        },
        "keywords": {
        "type": "string",
        "description": "Lista de palabras clave."
        },
        "enabled": {
        "type": "boolean",
        "description": "Servicio habilitado SI o NO."
        }
    }
    }

    """

    title = fields.Str(validate=validate.Length(max=30))
    description = fields.Str(validate=validate.Length(max=50))
    creation_date = fields.DateTime()
    close_date = fields.DateTime()
    status = fields.Enum(ServiceRequestStatus)

    @post_dump
    def dump_service(self, data, **kwargs):
        # Converting keywords list to string
        data["status"] = ServiceRequestStatus[data["status"]].value
        return data

    # keywords = fields.List(fields.String(validate=validate.Regexp(r"^[a-zA-Z0-9]+$")))
    # enabled = fields.Bool()


class CreateServiceSchema(Schema):
    """Creates Service Schema"""

    title = fields.Str(
        validate=validate.Length(max=30),
        required=True,
        error_messages={"required": {"message": "El título es requerido"}},
    )
    description = fields.Str(
        validate=validate.Length(max=50),
        required=True,
        error_messages={"required": {"message": "La descripción es requerida"}},
    )
    service_id = fields.Integer(
        required=True,
        error_messages={"required": {"message": "El id del servicio es requerido"}},
    )


class ServiceRequestNoteSchema(Schema):
    """Service Request Note Schema and validation for api"""

    note = fields.Str()
    id = fields.Integer()

    @post_dump
    def dump_service(self, data, **kwargs):
        # Converting keywords list to string
        data["text"] = data.pop("note")
        return data


class CreateServiceRequestNoteSchema(Schema):
    """Service Request Note Schema and validation for api"""

    text = fields.Str(
        validate=validate.Length(max=100),
        required=True,
        error_messages={
            "required": {"message": "El texto es requerida"},
            "max": "El texto no puede superar los 100 caracteres",
        },
    )


get_requests_schema = GetServiceSchema(many=True)
get_request_schema = GetServiceSchema()
create_request_schema = CreateServiceSchema()
get_request_note_schema = ServiceRequestNoteSchema()
create_request_note_schema = CreateServiceRequestNoteSchema()
