from flask import Blueprint, render_template, session, redirect, request, abort
import databaseTools.dbPreparedStatements

database = databaseTools.MYSQL()

clocksite = Blueprint("clock", __name__, template_folder="templates")


@clocksite.route("/clock")
def clock():
    username = session.get("username", None)
    userid = session.get("userID", None)

    delete = request.args.get("delete", None)
    edit = request.args.get("edit", None)
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

    if edit and alarmid:

        optionsHour, optionsMinute, selected, alarmhour, alarmminute, repeatoption, repeat0, repeat1, repeat2, repeat3, daylist, monday, tuesday, wednesday, thursday, friday, saturday, sunday, active, switch, sound0, sound1, sound2, sound3, alarmsound = "", "", "", "", "", "", "", "", "", "", [], "", "", "", "", "", "", "", "", "", "", "", "", "", ""

        rows = databaseTools.dbPreparedStatements.getAlarm(connectionInnerscope, str(userid), str(alarmid))

        for row in rows:
            alarmhour = str(row[2])
            alarmminute = str(row[3])
            repeatoption = str(row[4])
            alarmsound = str(row[5])
            active = str(row[6])
            daylist = row[7]

        for i in range(24):
            calc = i / 10

            if calc < 1:
                hour = "0" + str(i)

            else:
                hour = str(i)

            if hour == alarmhour:
                selected = "selected"
            else:
                selected = ""

            optionsHour = optionsHour + """
                <option value=" """ + hour + """ " """ + selected + """>""" + hour + """</option>
            """

        for i in range(60):
            calc = i / 10

            if calc < 1:
                minute = "0" + str(i)

            else:
                minute = str(i)

            if minute == alarmminute:
                selected = "selected"
            else:
                selected = ""

            optionsMinute = optionsMinute + """
                <option value=" """ + minute + """ " """ + selected + """>""" + minute + """</option>
            """

        if repeatoption == "0":
            repeat0 = "selected"
        elif repeatoption == "1":
            repeat1 = "selected"
        elif repeatoption == "2":
            repeat2 = "selected"
        elif repeatoption == "3":
            repeat3 = "selected"

            daylist = str(daylist).replace("[", "")
            daylist = daylist.replace("]", "")
            daylist = daylist.replace(",", "")

            daylist = list(daylist.split(" "))

            monday = daylist[0]
            tuesday = daylist[1]
            wednesday = daylist[2]
            thursday = daylist[3]
            friday = daylist[4]
            saturday = daylist[5]
            sunday = daylist[6]

            if monday == "True":
                monday = "checked"

            if tuesday == "True":
                tuesday = "checked"

            if wednesday == "True":
                wednesday = "checked"

            if thursday == "True":
                thursday = "checked"

            if friday == "True":
                friday = "checked"

            if saturday == "True":
                saturday = "checked"

            if sunday == "True":
                sunday = "checked"

        if active == "1":
            switch = "checked"

        if alarmsound == "0":
            sound0 = "selected"
        elif alarmsound == "1":
            sound1 = "selected"
        elif alarmsound == "2":
            sound2 = "selected"
        elif alarmsound == "3":
            sound3 = "selected"


        return render_template("editAlarm.html", optionsHour=optionsHour, optionsMinute=optionsMinute, repeat0=repeat0,repeat1=repeat1, repeat2=repeat2, repeat3=repeat3,
                               monday=monday, tuesday=tuesday, wednesday=wednesday, thursday=thursday, friday=friday, saturday=saturday, sunday=sunday, switch=switch,
                               sound0=sound0, sound1=sound1, sound2=sound2, sound3=sound3)

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
                                <a href="/clock?edit=True&alarmid=""" + alarmid + """"><i class="bi bi-wrench"></i></a>
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
