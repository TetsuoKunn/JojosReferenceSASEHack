from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import timedelta
from guilds.settings import API_KEY
from django.utils import timezone
import hashlib
import requests

baseurl = "http://127.0.0.1:5000"

# Create your views here.
def index(request):
    token = request.session.get("userid")
    print(token)
    return render(request ,"index.html")

def signin(request):
    return render(request, "signin.html")

def register(request):
    if request.method == "POST":
        context = {}
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        userid = request.POST.get("userid")
        pw = hashlib.sha256(request.POST.get("password").encode('utf-8')).hexdigest()
        try:
            response = requests.get(baseurl+f"/user/register?key={API_KEY}&firstname={firstname}&lastname={lastname}&username={userid}&pw={pw}")
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()
            print(data)
            index(request)
        except requests.exceptions.RequestException as e:
            error = JsonResponse({"error": str(e)}, status=500)
            context["error"] = error
    return render(request ,"register.html", context)

def profile_view(request):
    return render(request ,"profile.html")

def guild_view(request):
    return render(request ,"guild.html")

def post_view(request):
    return render(request ,"post.html")

def guild_creation_view(request):
    return render(request ,"guild_creation.html")

def guild_user_view(request):
    return render(request ,"guild_user.html")

def guild_user_owner_view(request):
    return render(request ,"guild_user_owner.html")

def messaging_view(request):
    return render(request ,"messaging.html")

def message_view(request):
    return render(request ,"message.html")