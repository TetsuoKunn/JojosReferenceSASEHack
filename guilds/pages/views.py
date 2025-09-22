from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import timedelta
from guilds.settings import API_KEY
from django.utils import timezone
import hashlib
import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage
import requests
from urllib.parse import urlencode

baseurl = "http://127.0.0.1:5000"

# Create your views here.
def index(request):
    return render(request ,"index.html")

def signin(request):
    context = {}
    if request.session.get("userid") != None:
        return redirect('index')
    if request.method == "POST":
        userid = request.POST.get("userid")
        context["userid_memory"] = userid
        pw = hashlib.sha256(request.POST.get("password").encode('utf-8')).hexdigest()
        response = requests.get(baseurl+f"/user/signin?key={API_KEY}&username={userid}&pw={pw}")
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        if data.get("error"):
            if "UNIQUE" in data.get("error"):
                context["error"] = "This username is taken"
                context["userid_memory"] = userid
        else:
            if data.get("username") != None:
                request.session["userid"] = data.get("username")
                return redirect('index')
            context["pw"] = "Your Password is incorrect."
    return render(request, "signin.html", context)

def register(request):
    context = {}
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        userid = request.POST.get("userid")
        pw = hashlib.sha256(request.POST.get("password").encode('utf-8')).hexdigest()
        response = requests.get(baseurl+f"/user/register?key={API_KEY}&firstname={firstname}&lastname={lastname}&username={userid}&pw={pw}")
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        if data.get("error"):
            if "UNIQUE" in data.get("error"):
                context["error"] = "This username is taken"
                context["firstname_memory"] = firstname
                context["lastname_memory"] = lastname
                context["userid_memory"] = userid
        else:
            return redirect('signin')
    return render(request ,"register.html", context)

def profile_view(request, username):
    urlparams = {
        "key" : API_KEY,
        "username" : username
    }
    username = username
    response = requests.get(baseurl+f"/user/profile?{urlencode(urlparams)}")
    data = response.json()
    if data == []:
        return redirect('index')
    response1 = requests.get(baseurl+f"/guild_from_user?{urlencode(urlparams)}")
    data1 = response1.json()
    if data1 == []:
        return redirect('index')
    return render(request ,"profile.html", {"data" : data, 'profile': username, "guilds": data1})

def post_create(request):
    context = {}
    if request.session.get("userid") == None:
        return redirect('signin')

    context = {}
    if request.method == "POST":
        text = request.POST.get("text")
        guild = request.POST.get("guild")
        urlparams = {
            "key" : API_KEY,
            "text" : text,
            "username" : request.session.get("userid")
        }
        if guild != "None":
            urlparams["guildname"] = guild
        response = requests.get(baseurl+f"/post/create?{urlencode(urlparams)}")
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        if data.get("error"):
            print(data.get("error"))
            return render(request ,"post_create.html", context)
        else:
            return redirect('index')
    return render(request, "post_create.html",context)

def guild_view(request, guildname):
    urlparams = {
        "key" : API_KEY,
        "username" : guildname
    }
    guildname = guildname
    response = requests.get(baseurl+f"/guild/profile?{urlencode(urlparams)}")
    data = response.json()
    if data == []:
        return redirect('index')
    return render(request ,"guild.html",  {"data" : data, 'profile': guildname,})

def post_view(request):
    return render(request ,"post.html")

def guild_creation_view(request):
    if request.session.get("userid") == None:
        return redirect('signin')
    context = {}
    if request.method == "POST":
        guildname = request.POST.get("guild_name")
        description = request.POST.get("desc")
        country = request.POST.get("country")
        state = request.POST.get("state")
        city = request.POST.get("city")
        urlparams = {
            "key" : API_KEY,
            "guildname" : guildname,
            "description" : description,
            "country" : country,
            "state" : state,
            "city" : city,
            "username" : request.session.get("userid")
        }
        response = requests.get(baseurl+f"/guild/register?{urlencode(urlparams)}")
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        if data.get("error"):
            context["guildname_memory"] = guildname
            context["description_memory"] = description
            return render(request ,"guild_creation.html", context)
        else:
            return redirect('index')
    return render(request ,"guild_creation.html", context)

def guild_user_view(request):
    return render(request ,"guild_user.html")

def guild_user_owner_view(request):
    return render(request ,"guild_user_owner.html")

def messaging_view(request):
    return render(request ,"messaging.html")

def message_view(request):
    return render(request ,"message.html")
