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
    pass

def profile_view(request):
    pass

def guild_view(request):
    pass

def post_view(request):
    pass

def guild_creation_view(request):
    pass

def guild_user_view(request):
    pass

def guild_user_owner_view(request):
    pass

def messaging_view(request):
    pass

def message_view(request):
    pass