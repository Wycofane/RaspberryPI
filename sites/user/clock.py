from flask import Blueprint, render_template, session, redirect, request, abort, url_for
import re
import databaseTools.dbPreparedStatements


database = databaseTools.MYSQL()

clocksite = Blueprint("clock", __name__, template_folder="templates")


@clocksite.route("/clock")
def clock():
    username = session.get("username", None)
    userid = session.get("userID", None)

    delete = request.args.get("delete", None)
    alarmid = request.args.get("alarmid", None)

    modal = request.args.get("modal", None)
    hour = request.args.get("hour", None)
    minute = request.args.get("minute", None)

    alarms, modaltext = "", False

    if not username or not userid:
        return redirect("/")

    if modal and hour and minute:
        modaltext = "Your alarm was set to " + hour + ":" + minute

    connectionInnerscope = database.createConnection()
    rows = databaseTools.dbPreparedStatements.getUser(connectionInnerscope, username)

    for row in rows:
        username = row[1]

    if delete and alarmid:
        databaseTools.dbPreparedStatements.deleteAlarm(connectionInnerscope, userid, alarmid)

        return redirect("/clock")

    rows = databaseTools.dbPreparedStatements.getAlarms(connectionInnerscope, str(userid))

    for row in rows:
        alarmid = str(row[0])
        alarmhour = str(row[2])
        alarmminute = str(row[3])
        repeatoption = str(row[4])
        alarmsound = str(row[5])
        active = str(row[6])
        daylist = row[7]

        if active == "0":
            active = "Deactivated"

        elif active == "1":
            active = "Active"

        else:
            print("active?")
            abort(500)

        if alarmsound == "0":
            alarmsound = "Classic"

        elif alarmsound == "1":
            alarmsound = "WAKE UP"

        elif alarmsound == "2":
            alarmsound = "Star Wars"

        elif alarmsound == "3":
            alarmsound = "Londonbridges"
        else:
            print("alarmsound?")
            abort(500)


        if repeatoption == "0":
            repeatoption = "Just once"

        elif repeatoption == "1":
            repeatoption = "Repeat everyday(mo - sun)"

        elif repeatoption == "2":
            repeatoption = "Repeat workdays(mo - fr)"

        elif repeatoption == "3":

            daylist = str(daylist).replace("[", "")
            daylist = daylist.replace("]", "")
            daylist = daylist.replace(",", "")

            daylist = list(daylist.split(" "))

            repeatoption, days = "", ""

            monday = daylist[0]
            tuesday = daylist[1]
            wednesday = daylist[2]
            thursday = daylist[3]
            friday = daylist[4]
            saturday = daylist[5]
            sunday = daylist[6]

            if monday == "True":
                days = days + " monday"

            if tuesday == "True":
                days = days + " tuesday"

            if wednesday == "True":
                days = days + " wednesday"

            if thursday == "True":
                days = days + " thursday"

            if friday == "True":
                days = days + " friday"

            if saturday == "True":
                days = days + " saturday"

            if sunday == "True":
                days = days + " sunday"

            if days == "":
                days = "no repeat days selected"

            repeatoption = days

        else:
            print("repeatoption?")
            abort(500)


        alarms = alarms + """
        
            <div class="col-sm-3">
					<div class="card">
                        <div class="card-header">
                            Alarm - """ + active + """
                            <div class="text-end">
                                <a href="/clock?edit=True&alarmid=""" + alarmid + """"><i class="bi bi-trash"></i></a>
                                <a href="/clock?delete=True&alarmid=""" + alarmid + """"><i class="bi bi-trash"></i></a>
                            </div>
                        </div>
                        <div class="card-body border border-2">
                            <p class="card-text"> """ + alarmhour + """ : """ + alarmminute + """</p>
                            <p class="card-text"> Alarmsound: """ + alarmsound + """</p>
                            <p class="card-text"> Repeat: """ + repeatoption + """</p>
                        </div>
                    </div>
			</div>
            
        """







    return render_template("clock.html", username=username, alarms=alarms, modaltext=modaltext)
