from flask import Flask, request, abort, jsonify
from markupsafe import escape
from django.utils import timezone
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


@app.route("/user/joinguild")
def join_guild():
    key = request.headers.get("X-API-KEY") or request.args.get("key")
    security_check(key)
    username = request.args.get("username")
    guildName = request.args.get("guildname")
    creationDate = datetime.now()
    try:
        db.joinGuild(username, guildName, creationDate)
    except Exception as e:
        data = {
            "error": str(e),
            "type": e.__class__.__name__
        }
        return jsonify(data)
    data = {}
    return jsonify(data)


@app.route("/search/country")
def countrySearch():
    key = request.headers.get("X-API-KEY") or request.args.get("key")
    security_check(key)
    guildname = request.args.get("guildname")
    try:
        rows = db.getAllGuildsCountry(guildname)
        data = [
            {
                "name": r[0],
                "description": r[1],
            }
            for r in rows
        ]
    except Exception as e:
        data = {
            "error": str(e),
            "type": e.__class__.__name__
        }
        return jsonify(data)
    return jsonify(data)

@app.route("/search/state")
def stateSearch():
    key = request.headers.get("X-API-KEY") or request.args.get("key")
    security_check(key)
    guildname = request.args.get("guildname")
    try:
        rows = db.getAllGuildsState(guildname)
        data = [
            {
                "name": r[0],
                "description": r[1],
            }
            for r in rows
        ]
    except Exception as e:
        data = {
            "error": str(e),
            "type": e.__class__.__name__
        }
        return jsonify(data)
    return jsonify(data)

@app.route("/search/city")
def citySearch():
    key = request.headers.get("X-API-KEY") or request.args.get("key")
    security_check(key)
    guildname = request.args.get("guildname")
    try:
        rows = db.getAllGuildsCity(guildname)
        data = [
            {
                "name": r[0],
                "description": r[1],
            }
            for r in rows
        ]
    except Exception as e:
        data = {
            "error": str(e),
            "type": e.__class__.__name__
        }
        return jsonify(data)
    return jsonify(data)


@app.route("/guild/allusers")
def showAllUsers():
    key = request.headers.get("X-API-KEY") or request.args.get("key")
    security_check(key)
    guildname = request.args.get("guildname")
    try:
        rows = db.getAllUsersInGuild(guildname)

        data = [
            {
                "username": r[0],
                "firstname": r[1],
                "lastname": r[2],
                "role": r[3],
                "datejoined": r[4],
            }
            for r in rows
        ]
    except Exception as e:
        data = {
            "error": str(e),
            "type": e.__class__.__name__
        }
        return jsonify(data)
    return jsonify(data)


@app.route("/user/profile")
def UserProfilePage():
    key = request.headers.get("X-API-KEY") or request.args.get("key")
    security_check(key)
    username = request.args.get("username")
    try:
        rows = db.getAllPostsUser(username)

        data = [
            {
                "postID": r[0],
                "username": r[1],
                "text": r[2],
                "pictureID": r[3],
                "creationDate": r[4],
                "likes": r[5],
            }
            for r in rows
        ]
    except Exception as e:
        data = {
            "error": str(e),
            "type": e.__class__.__name__
        }
        return jsonify(data)
    return jsonify(data)


@app.route("/guild/profile")
def GuildProfilePage():
    key = request.headers.get("X-API-KEY") or request.args.get("key")
    security_check(key)
    guildname = request.args.get("guildname")
    try:
        rows = db.getAllPostsGuild(guildname)

        data = [
            {
                "postID": r[0],
                "name": r[1],
                "text": r[2],
                "pictureID": r[3],
                "creationDate": timezone.make_aware(datetime.fromisoformat(r[4])),
                "likes": r[5],
            }
            for r in rows
        ]
    except Exception as e:
        data = {
            "error": str(e),
            "type": e.__class__.__name__
        }
        return jsonify(data)
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

@app.route("/guild_from_user")
def guild_from_user():
    data = {}
    key = request.args.get("key")
    security_check(key)
    username = request.args.get("username")
    try:
        guilds = db.getGuildsfromUser(username)
        guilds_json = [{"name": g[0], } for g in guilds]
        data = {"guilds": guilds_json}
    except Exception as e:
        data = {
            "error": str(e),
            "type": e.__class__.__name__
        }
        return jsonify(data)
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
