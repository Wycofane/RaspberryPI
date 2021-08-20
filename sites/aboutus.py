from flask import Blueprint, render_template

aboutussite = Blueprint("aboutUs", __name__, template_folder="templates")


@aboutussite.route("/aboutus", methods=["GET"])
def aboutUs():

    return render_template("aboutus.html")
