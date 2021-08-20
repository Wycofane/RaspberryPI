from flask import Blueprint, render_template, session, redirect, request, abort, url_for
import re
import databaseTools.dbPreparedStatements


database = databaseTools.MYSQL()

profilesite = Blueprint("profile", __name__, template_folder="templates")


@profilesite.route("/profile")
def profile():
    username = session.get("username", None)

    if not username:
        return redirect("/")

    connectionInnerscope = database.createConnection()
    rows = databaseTools.dbPreparedStatements.getUser(connectionInnerscope, username)

    for row in rows:
        username = row[1]


    return render_template("profile.html", username=username)
