from flask import Blueprint, session, redirect, url_for, render_template
import sensitiveData as sd

indexPage = Blueprint("index", __name__, template_folder="templates")


@indexPage.route("/")
def index():
    email = session.get("email", "")

    if email:
        if email and not email in sd.email and email != "":  # User is logged in and not the admin
            return redirect(url_for("profile.profile"))


    return render_template("index.html")
