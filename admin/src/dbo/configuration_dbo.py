from src.core.database import db
from src.models.configuration import ConfigurationModel


def get_per_page():
    """Get the number of elements per page"""
    config = ConfigurationModel.query.first()
    if config is None:
        return 4  # Default
    return config.elements_per_page


def get_maintenance_mode():
    """Get whether the application is in maintenance mode"""
    config = ConfigurationModel.query.first()
    if config is None:
        return False  # Default
    return config.maintenance_mode


def get_phone_number():
    """Get the contact phone number"""
    config = ConfigurationModel.query.first()
    if config is None:
        return "-"  # Default
    return config.phone_number


def get_email():
    """Get the contact email"""
    config = ConfigurationModel.query.first()
    if config is None:
        return "-"  # Default
    return config.email


def get_maintenance_message():
    """Get the maintenance message"""
    config = ConfigurationModel.query.first()
    if config is None:
        return "-"  # Default
    return config.maintenance_message


def get_configuration():
    """Get the system configuration"""
    config = ConfigurationModel.query.first()
    return config


def update_configuration(data):
    """Update the system configuration"""
    config = ConfigurationModel.query.first()
    if config is None:
        # If there is no configuration in the database, create one
        config = ConfigurationModel(
            elements_per_page=data.get("elements_per_page"),
            phone_number=data.get("phone_number"),
            email=data.get("email"),
            maintenance_mode=data.get("maintenance_mode"),
            maintenance_message=data.get("maintenance_message"),
        )
        db.session.add(config)
    else:
        # If a configuration already exists, update its fields
        config.elements_per_page = data.get("elements_per_page")
        config.phone_number = data.get("phone_number")
        config.email = data.get("email")
        config.maintenance_mode = data.get("maintenance_mode")
        config.maintenance_message = data.get("maintenance_message")

    db.session.commit()
    return config
