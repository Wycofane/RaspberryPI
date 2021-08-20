from flask import Blueprint, session, redirect, url_for, render_template
import sensitiveData as sd

indexPage = Blueprint("index", __name__, template_folder="templates")


@indexPage.route("/")
def index():
    username = session.get("username", "")

    if username:
        if username and username != "":  # User is logged in and not the admin
            return redirect(url_for("profile.profile"))


    return render_template("index.html")
