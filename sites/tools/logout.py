from flask import Blueprint, session, g, redirect

logout = Blueprint("logout", __name__, template_folder="templates")


@logout.route("/logout")
def logoutAction():
    g.user = None

    session.pop("username", "")
    session.pop("userID", "")

    return redirect("/")
