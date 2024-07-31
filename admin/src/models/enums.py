from enum import Enum


class UserDocument(Enum):
    DNI = "DNI"
    CIVIC = "Libreta Cívica"
    ENROLMENT = "Libreta de Enrolamiento"


class UserGender(Enum):
    MALE = "Masculino"
    FEMALE = "Femenino"
    OTHER = "Otros (Por favor especifica)"
    NOT_SPECIFIED = "Prefiero no decir"


class Roles(Enum):
    OWNER = "OWNER"
    ADMINISTRATOR = "ADMINISTRATOR"
    OPERATOR = "OPERATOR"
    SUPERADMIN = "SUPERADMIN"


class Operations(Enum):
    USER = "user"
    INSTITUTION = "institution"
    INSTITUTION_USER = "institution_user"
    SERVICE = "service"
    SERVICE_REQUEST = "service_request"
    CONFIG = "config"

    @property
    def index(self):
        return f"{self.value}_index"

    @property
    def create(self):
        return f"{self.value}_create"

    @property
    def delete(self):
        return f"{self.value}_delete"

    @property
    def update(self):
        return f"{self.value}_update"

    @property
    def show(self):
        return f"{self.value}_show"


class ServiceTypes(Enum):
    ANALYSIS = "Analisis"
    CONSULTING = "Consultoria"
    DEVELOPMENT = "Desarrollo"


class ServiceRequestStatus(Enum):
    ACCEPTED = "Aceptado"
    REJECTED = "Rechazado"
    PENDING = "En proceso"
    CANCELED = "Cancelado"
    FINISHED = "Finalizado"
