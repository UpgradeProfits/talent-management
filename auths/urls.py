from django.urls import path
from auths import views

urlpatterns = [
    path('', views.sign_up, name="sign-up"),
    path('user/', views.get_details, name='get_details'),
    #
    path('category/', views.user_categories, name='category')
]