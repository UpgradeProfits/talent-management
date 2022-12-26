from django.urls import path
from auths import views

urlpatterns = [
    # SignUp urls
    path('signup/', views.sign_up_view, name="sign-up"),
    path('user/', views.sign_up),#this is the url that ajax sends the users detail to for authentication @ the sign_up view
    # SignIn urls
    path('signin/', views.sign_in_view, name="login"),
    path('login/', views.sign_in),#this is the url that ajax sends the users detail to for authentication @ the sign_in view
    #
    path('category/', views.user_categories, name='category')
]