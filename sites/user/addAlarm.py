from flask import Blueprint, render_template, session, redirect, request, abort, url_for
import re
import databaseTools.dbPreparedStatements


database = databaseTools.MYSQL()

addAlarmsite = Blueprint("addAlarm", __name__, template_folder="templates")


@addAlarmsite.route("/addAlarm", methods=["GET", "POST"])
def addAlarm():
    username = session.get("username", None)
    userid = session.get("userID", None)

    if not username or not userid:
        return redirect("/")

    connectionInnerscope = database.createConnection()
    rows = databaseTools.dbPreparedStatements.getUser(connectionInnerscope, username)

    for row in rows:
        username = row[1]

    if request.method == "POST":

        alarmhour = request.form.get("alarmhour", None)
        alarmminute = request.form.get("alarmminute", None)
        repeatoption = request.form.get("repeatoption", None)
        alarmsound = request.form.get("alarmsound", None)

        monday, tuesday, wednesday, thursday, friday, saturday, sunday, daylist = False, False, False, False, False, False, False, ""

        if repeatoption == "3":
            if request.form.getlist("option1check"):
                monday = True
            if request.form.getlist("option2check"):
                tuesday = True
            if request.form.getlist("option3check"):
                wednesday = True
            if request.form.getlist("option4check"):
                thursday = True
            if request.form.getlist("option5check"):
                friday = True
            if request.form.getlist("option6check"):
                saturday = True
            if request.form.getlist("option7check"):
                sunday = True

            daylist = [monday, tuesday, wednesday, thursday, friday, saturday, sunday]

        if alarmhour and alarmminute and repeatoption and alarmsound:
            databaseTools.dbPreparedStatements.insertIntoAlarms(connectionInnerscope, userid, alarmhour, alarmminute, repeatoption, alarmsound, str(daylist))


            return redirect("/clock?modal=True&hour=" + alarmhour + "&minute=" + alarmminute)

    return render_template("addAlarm.html", username=username)
