from flask import Blueprint, render_template

servicessite = Blueprint("services", __name__, template_folder="templates")


@servicessite.route("/services", methods=["GET"])
def services():

    return render_template("services.html")
