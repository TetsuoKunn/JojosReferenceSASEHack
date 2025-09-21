from flask import Flask, request, abort, jsonify
from markupsafe import escape
from MessageDatabase import *
from datetime import datetime
# from User import *
from dotenv import load_dotenv
import os

# flask --app app run --debug

load_dotenv("../")
API_KEY = os.getenv("API_KEY")
db = DatabaseHelper()
db.connectToDataBase()
db.createTables()
def security_check(key):
    if(key != API_KEY):
        abort(403)

app = Flask(__name__)

# The following is the easiest way to implement a url that performs CRUD operations
@app.route("/")
def hello_world():
    key = request.headers.get("X-API-KEY") or request.args.get("key")
    name = request.args.get("name")
    security_check(key)
    return f"hello, {escape(name)}"

@app.route("/user/register")
def register():
    key = request.headers.get("X-API-KEY") or request.args.get("key")
    security_check(key)
    username = request.args.get("username")
    firstname = request.args.get("firstname")
    lastname = request.args.get("lastname")
    password = request.args.get("pw")
    joiningDate = datetime.now()
    try:
        db.register(username, firstname, lastname, password, joiningDate)
    except Exception as e:
        data = {
            "error": str(e),
            "type": e.__class__.__name__
        }
        return jsonify(data)
    data = {"username" : username}
    return jsonify(data)

@app.route("/user/signin")
def login():
    key = request.headers.get("X-API-KEY") or request.args.get("key")
    security_check(key)
    username = request.args.get("username")
    password = request.args.get("pw")
    try:
        true = db.login(username, password)
    except Exception as e:
        data = {
            "error": str(e),
            "type": e.__class__.__name__
        }
        return jsonify(data)
    if true:
        data = {"username" : username}
    else:
        data = {}
    return jsonify(data)

@app.route("/guild/register")
def guild_create():
    key = request.headers.get("X-API-KEY") or request.args.get("key")
    security_check(key)
    username = request.args.get("username")
    guildName = request.args.get("guildname")
    description = request.args.get("description")
    country = request.args.get("country")
    state = request.args.get("state")
    city = request.args.get("city")
    creationDate = datetime.now()
    try:
        db.registerGuild(guildName, username, creationDate, description, country, state, city)
    except Exception as e:
        data = {
            "error": str(e),
            "type": e.__class__.__name__
        }
        return jsonify(data)
    data = {}
    return jsonify(data)

@app.route("/post/create")
def post_create():
    data = {}
    key = request.args.get("key")
    security_check(key)
    username = request.args.get("username")
    guildName = request.args.get("guildname", "-1")
    pictureID = request.args.get("picture", "-1")
    creationDate = datetime.now()
    text = request.args.get("text")
    try:
        db.newPost(username, guildName, text, creationDate, pictureID)
    except Exception as e:
        data = {
            "error": str(e),
            "type": e.__class__.__name__
        }
        return jsonify(data)
    data = {}
    return jsonify(data)

# @app.route("/<appropriate_url>")
# def <function_name>():
#     variable = request.args.get("variable", "default")
#     below is required to ensure some form of sofety
#     key = request.headers.get("X-API-KEY") or request.args.get("key")
#     security_check(key)
#     run_username_func(variable)
#     """ will run the function if username provided is in the url in the form of /<appropriateurl>?variable=henry"""
#     the return function could just be a confirmation or it could be returning any appropriate data
#     return f"hello, {escape(name)}"

# Add as many variables as you need
# last_name = request.args.get("last", "App")
# age = request.args.get("age", "unknown")
# here app and unknown are default values incase the user doesn't enter them
