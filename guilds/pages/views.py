from django.shortcuts import render
from django.http import HttpResponse
from datetime import timedelta
from django.utils import timezone


# Create your views here.
def index(request):
    token = request.session.get("userid")
    print(token)
    return render(request ,"index.html")

def signin(request):
    request.session['userid'] = "112255"
    return render(request, "signin.html")

def register(request):
    return render(request ,"register.html")

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