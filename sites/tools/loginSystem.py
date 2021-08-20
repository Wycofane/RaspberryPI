from flask import Blueprint, render_template, session, redirect, request, abort, url_for
import hashlib
import databaseTools.dbPreparedStatements
import globals as variable


database = databaseTools.MYSQL()

login = Blueprint("welcome", __name__, template_folder="templates")


@login.route("/login", methods=["GET", "POST"])
def welcome():
    error = variable.loginerror
    addr = str(request.remote_addr)

    userid = session.get("userid", None)

    # build a connection to the DB with failsave
    connectionInnerScope = database.createConnection()

    linkBack = request.args.get("linkback", None)

    if userid:
        return redirect("/")

    if request.method == "POST":

        variable.loginerror = None

        # remove the email from the session
        session.pop("userID", None)
        session.pop("username", None)

        # request the data typed in
        usernameInput = request.form.get("username", None)

        passwordInput = request.form.get("password", None)

        if usernameInput is None or passwordInput is None:
            abort(500)

        usernameInput = usernameInput.lower()

        maliciousChars = ["(", ")", ";", "="]

        lenMC = len(maliciousChars)

        for i in range(lenMC - 1):
            if maliciousChars[i] in usernameInput:

                if not addr in variable.ipBan:
                    variable.ipBan.append(addr)
                    abort(403)
                elif addr in variable.ipBan:
                    variable.ipBan2.append(addr)
                    abort(403)
                else:
                    abort(403)


        # convert the password to a md5 hash
        passwordInput = hashlib.md5(passwordInput.encode()).hexdigest()

        # get the user from the db
        values = databaseTools.dbPreparedStatements.getUser(connectionInnerScope, usernameInput)

        # iterate through the user
        for row in values:

            # get the data from the user (db)object
            userID = str(row[0])
            username = row[1]
            password = row[2]

            # check if the datas are the same (basic login stuff)
            if password == passwordInput and username == usernameInput:

                # if yes add the user to the session
                session["username"] = username
                session["userID"] = userID

                if linkBack:
                    return redirect(url_for(linkBack))

                return redirect("/profile")

        error = "Wrong login credentials please try again!"

    return render_template("loginform.html", error=error)  # render a the loginform template
