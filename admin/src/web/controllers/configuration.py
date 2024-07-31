from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from src.dbo import configuration_dbo
from src.models.enums import Operations
from src.web.utils import session
from src.web.utils.auth import validate_operation
from src.web.utils.forms.configuration import ConfigurationUpdateForm

configuration_routing = Blueprint(
    "configuration",
    __name__,
    static_folder="static",
    template_folder="templates/configuration",
)


@configuration_routing.route("/configuration", methods=["GET", "POST"])
@validate_operation(Operations.CONFIG.show)
def configuration_page():
    """Returns the configuration page"""

    config = configuration_dbo.get_configuration()
    form = ConfigurationUpdateForm(request.form)

    if request.method == "POST" and form.validate():
        new_config_data = form.data
        new_config_data["elements_per_page"] = float(
            new_config_data["elements_per_page"]
        )
        configuration_dbo.update_configuration(new_config_data)
        flash("Configuración actualizada exitosamente!", "success")
        return redirect(url_for("configuration.configuration_page"))

    return render_template(
        "configuration/configuration-page.html",
        config=config,
        form=form,
    )


@configuration_routing.route("/configuration/edit", methods=["GET", "POST"])
@validate_operation(Operations.CONFIG.update)
def edit_configuration():
    """Returns the configuration editor page"""

    config = configuration_dbo.get_configuration()
    form = ConfigurationUpdateForm(request.form, obj=config)

    if request.method == "POST" and form.validate():
        configuration_data = {
            "elements_per_page": form.elements_per_page.data,
            "phone_number": form.phone_number.data,
            "email": form.email.data,
            "maintenance_mode": form.maintenance_mode.data,
            "maintenance_message": form.maintenance_message.data,
        }
        print(configuration_data)

        configuration_dbo.update_configuration(configuration_data)
        flash("Configuración actualizada exitosamente!", "success")
        return redirect(url_for("configuration.configuration_page"))

    return render_template(
        "configuration/configuration-update.html",
        form=form,
    )
