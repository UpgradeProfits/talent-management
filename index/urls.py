from django.urls import path
from index import views

urlpatterns = [
    path('', views.index, name="home"),
    path('render_data/', views.render_data, name="render_data"),
]