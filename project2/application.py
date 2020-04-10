import os
import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, flash, url_for
from flask_session import Session
from flask_socketio import SocketIO, emit
from functools import wraps


app = Flask(__name__)

app.config["SECRET_KEY"] = "my secret key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)
socketio = SocketIO(app)

users = {}
channels = {}
all_channels = []
channelMessages = {}
user_ids = []


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        session.clear()
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users and users[username] == str(password):
            session["user_name"] = username
            channels[session["user_name"]] = set()
            return render_template("home.html", username=username, channels=channels[session["user_name"]]
                                   , all_channels=all_channels, channelMessages=channelMessages)
        else:
            flash("Wrong username or password", "danger")
            return render_template("login.html")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users:
            flash("Username already exists!", "danger")
            return render_template("register.html")
        elif len(password) == 0 or len(username) == 0:
            flash("Credentials are not valid", "danger")
            return render_template("register.html")
        else:
            flash("Congrats, you have created your account. Login now!", "success")
            users[username] = password
            return render_template("login.html")


@app.route("/")
def index():
    return render_template("index.html")


@login_required
@app.route("/home")
def home():
    return render_template("home.html", username=session["user_name"], channels=channels[session["user_name"]],
                           all_channels=all_channels, channelMessages=channelMessages)


@login_required
@app.route("/create", methods=['GET', 'POST'])
def create_new_channel():
    if request.method == 'POST':
        channel_id = str(request.form.get("channelId"))
        if channel_id not in channels:
            session["channel_id"] = channel_id
            channelMessages[channel_id] = []
            channels[session["user_name"]].add(channel_id)
            all_channels.append(channel_id)
            print(channels)
            flash("Channel created", "success")
            return redirect(url_for("home", channels=channels, channelMessages=channelMessages[session["channel_id"]]))
        else:
            flash("Sorry, channel is already exist!", "danger")
            return render_template("create_channel.html", channels=channels[session["user_name"]],
                                   all_channels=all_channels, username=session["user_name"])
    else:
        return render_template("create_channel.html", channels=channels[session["user_name"]],
                               all_channels=all_channels)


@login_required
@app.route("/channels/<string:channel>", methods=["GET", "POST"])
def change_channel(channel):
    # current = time.asctime(time.localtime(time.time()))
    # current = datetime.datetime.now()
    # current = (str(current.hour) + ":" + str(current.minute) + ":" + str(current.second))
    # current = current.strftime("%I:%M:%S %p")
    # notify = str(current) + ": User has joined"
    session["channel_id"] = channel
    return render_template("home.html", channel=channel, channels=channels[session["user_name"]],
                           all_channels=all_channels, username=session["user_name"],
                           channelMessages=channelMessages[session["channel_id"]])


@login_required
@app.route("/leave/<string:channel>")
def leave(channel):
    channels[session["user_name"]].remove(channel)
    all_channels.remove(channel)
    return render_template("home.html", channels=channels[session["user_name"]], all_channels=all_channels)


@login_required
@app.route("/join/<string:channel>")
def join_channel(channel):
    session["channel_id"] = channel
    return render_template("home.html", channel=channel, channels=channels[session["user_name"]],
                           all_channels=all_channels, channelMessages=channelMessages[session["channel_id"]])


@socketio.on("user connected")
def connect(msg):
    print(msg)
    emit("user connected", msg, broadcast=True)
    return


@socketio.on("join room")
def join(timestamp):
    if session["channel_id"] not in channels[session["user_name"]]:
        channels[session["user_name"]].add(session["channel_id"])
        msg = session['user_name'] + " [" + timestamp + "]: " + " has joined the room"
        channelMessages[session["channel_id"]].append(msg)
        emit("joined room", msg, broadcast=True)


@socketio.on("send msg")
def send(msg):
    new_msg = session["user_name"] + " " + msg
    channelMessages[session["channel_id"]].append(new_msg)
    emit("msg sent", new_msg, broadcast=True)
