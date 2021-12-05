from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, static_folder="static")
app.config['SECRET_KEY'] = 'SAJF3924MVZX!0-1924JKALSMFCKNBSAUIUHFW'
socket_app = SocketIO(app)
