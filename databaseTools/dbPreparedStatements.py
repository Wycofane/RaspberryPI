# get how many row the table have
def getRowCount(connection, tablename):
    # create a cursor
    dbcur = connection.cursor()
    # execute the SQL statment to get every entry of a specific table
    dbcur.execute("SELECT * FROM " + tablename)
    # get everything
    dbcur.fetchall()
    # count everything
    rowcount = dbcur.rowcount
    # return the counter
    return rowcount


# universal function to get a user from the DB
def getUsersFromDB(connection, wherecondition):
    dbcur = connection.cursor()

    dbcur.execute("SELECT * FROM users where " + wherecondition)
    record = dbcur.fetchall()
    dbcur.close()

    return record


# static function to get a User by its email
def getUser(connection, username):
    dbcur = connection.cursor()

    dbcur.execute("SELECT * FROM users where username = " + "'" + username + "'")

    record = dbcur.fetchall()
    dbcur.close()

    return record


# static function to get a User by its email
def getUserByID(connection, userid):
    dbcur = connection.cursor()

    dbcur.execute("SELECT * FROM users where userID = " + "'" + userid + "'")

    record = dbcur.fetchall()
    dbcur.close()

    return record


# function to add the user into the DB
def insertIntoUsers(connection, userid, password, username):
    dbcur = connection.cursor()

    dbcur.execute(
        "INSERT INTO users (userID, password, username) VALUES ('" + userid + "','" + password + "','" + username + "');")

    connection.commit()
    dbcur.close()


# function to add the alarm into the DB
def insertIntoAlarms(connection, userid, alarmhour, alarmminute, repeatoption, alarmsound, daylist):
    dbcur = connection.cursor()

    if not daylist:
        daylist = ""

    dbcur.execute(
        "INSERT INTO alarms (userID, alarmhour, alarmminute, repeatoption, alarmsound, active, daylist) VALUES ('" + userid + "','" + alarmhour + "','" + alarmminute + "','" + repeatoption + "','" + alarmsound + "','" + str(1) + "','" + daylist + "');")

    connection.commit()
    dbcur.close()


def deleteAlarm(connection, userID, alarmid):
    dbcur = connection.cursor()

    dbcur.execute(
        "DELETE FROM alarms where userID = " + "'" + userID + "'" + " and alarmid = " + "'" + alarmid + "'"
    )

    connection.commit()

    dbcur.close()


# static function to get the alarm by userID
def getAlarms(connection, userid):
    dbcur = connection.cursor()

    dbcur.execute("SELECT * FROM alarms where userID = " + "'" + userid + "'")

    record = dbcur.fetchall()
    dbcur.close()

    return record


# static function to get the alarm by userID and alarmID
def getAlarm(connection, userid, alarmid):
    dbcur = connection.cursor()

    dbcur.execute("SELECT * FROM alarms where userID = " + "'" + userid + "' AND alarmid = " + "'" + alarmid + "'")

    record = dbcur.fetchall()
    dbcur.close()

    return record