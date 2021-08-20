import sensitiveData as sd
import globals as variable
import databaseTools.dbPreparedStatements

from flask import Flask, session, render_template, request, abort, redirect, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from sites.aboutus import aboutussite
from sites.services import servicessite

from sites.user.profile import profilesite
from sites.tools.logout import logout
from sites.tools.loginSystem import login

from sites.indexPage import indexPage


database = databaseTools.MYSQL()

# Initialize the Flask APP
app = Flask(__name__)

app.secret_key = sd.secretKey

limiter = Limiter(
    app,
    key_func=get_remote_address,
)

app.register_blueprint(indexPage)
app.register_blueprint(aboutussite)
app.register_blueprint(servicessite)
app.register_blueprint(profilesite)
app.register_blueprint(logout)


limiter.limit("60 per hour")(login)
app.register_blueprint(login)


@app.route("/test/<text>")
def test(text):

    return text


@app.errorhandler(403)
def forbidden(e):
    # Check if the user is in the global context logged in if yes redirect to the page but with changed layout
    loggedin, nav = False, False

    username = session.get("username", None)

    if username:
        loggedin = True

    return render_template('403.html', loggedin=loggedin), 403


@app.errorhandler(404)
def page_not_found(e):
    # Check if the user is in the global context logged in if yes redirect to the page but with changed layout
    loggedin, nav = False, False

    username = session.get("username", None)

    if username:
        loggedin = True

    return render_template('404.html', loggedin=loggedin), 404


@app.errorhandler(429)
def tooManyReq(e):
    # Check if the user is in the global context logged in if yes redirect to the page but with changed layout
    loggedin, nav = False, False

    username = session.get("username", None)

    if username:
        loggedin = True

    return render_template('429.html', loggedin=loggedin), 429


@app.errorhandler(500)
def serverfailure(e):
    # Check if the user is in the global context logged in if yes redirect to the page but with changed layout
    loggedin, nav = False, False

    username = session.get("username", None)

    if username:
        loggedin = True

    return render_template('500.html', loggedin=loggedin), 500


@app.before_request
def before_request():

    addr = str(request.remote_addr)

    if addr in variable.ipBan2:
        abort(403)


def createApp():
    print("by Wycofane 2021")

    app.run(host="0.0.0.0", port=80)
