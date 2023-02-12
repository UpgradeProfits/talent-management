
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat-home'),
    # path('chat/', views.box, name='chatbox'),
    path('profile/', views.profile, name='chat-profile'),
    path('send/', views.send_chat, name='chat-send'),
    path('renew/', views.get_messages, name='chat-renew'),
]
