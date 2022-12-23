from django.urls import path
from auth import views

urlpatterns = [
    path('', views.sign_up, name="sign-up")
]