"""
URL configuration for guilds project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pages.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('signin/' ,signin, name="signin"),
    path('register/', register, name="register"),
    path('profile/', profile_view, name="profile"),
    path("guild/", guild_view, name="guild"),
    path("post/", post_view, name="post"),
    path("post/create", post_create, name="post_create"),
    path("guild/create/", guild_creation_view, name="guild_create"),
    path("guild/user/", guild_user_view, name="guild_user"),
    path("guild/user/owner/", guild_user_owner_view, name="guild_user_owner"),
    path("messages/", messaging_view, name="messages"),
    path("message/", message_view, name="message"),

]
