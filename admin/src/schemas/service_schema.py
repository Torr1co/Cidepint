from marshmallow import Schema, fields, post_dump, validate

from src.models.enums import ServiceTypes


class ServiceSchema(Schema):
    """Service Schema"""

    name = fields.Str(validate=validate.Length(max=30))
    description = fields.Str(validate=validate.Length(max=50))
    laboratory = fields.Str(validate=validate.Length(max=30))
    keywords = fields.List(fields.String(validate=validate.Regexp(r"^[a-zA-Z0-9]+$")))
    enabled = fields.Bool()

    @post_dump
    def dump_service(self, data, **kwargs):
        # Converting keywords list to string
        data["keywords"] = ",".join(data["keywords"])
        return data


class ServiceAnalisisSchema(ServiceSchema):
    """Service Schema for analisis"""

    request_count = fields.Integer()


class ServiceTypesAnalisisSchema(Schema):
    """Service Schema for analisis"""

    service_type = fields.Enum(ServiceTypes)
    request_count = fields.Integer()

    @post_dump
    def dump_service_type(self, data, **kwargs):
        # Converting keywords list to string
        data["service_type"] = ServiceTypes[data["service_type"]].value
        return data


get_services_schema = ServiceSchema(many=True)
get_service_schema = ServiceSchema()
service_analisis_schema = ServiceAnalisisSchema(many=True)
service_types_analisis_schema = ServiceTypesAnalisisSchema(many=True)
