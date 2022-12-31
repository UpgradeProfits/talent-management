from django.urls import path
from auths import views
from django.contrib.auth import views as django_views

urlpatterns = [
    # SignUp urls
    path('signup/', views.sign_up_view, name="sign-up"),
    path('user/', views.sign_up),#this is the url that ajax sends the users detail to for authentication @ the sign_up view
    # SignIn urls
    path('signin/', views.sign_in_view, name="login"),
    path('login/', views.sign_in),#this is the url that ajax sends the users detail to for authentication @ the sign_in view
    #Reset Password url
    path('password_reset/', django_views.PasswordResetView.as_view(), name="reset_password"),
    path('password_reset_sent/', django_views.PasswordResetDoneView.as_view(), name="reset_done"),
    path('reset/<uidb64>/<token>/', django_views.PasswordResetConfirmView.as_view(), name="reset_confirm"),
    path('reset_complete/', django_views.PasswordResetCompleteView.as_view(), name="reset_complete"),
    #
    path('category/', views.user_categories, name='category'),
    path('createprofile/', views.createProfile, name="c_profile"),
    path('createdprofile/', views.userProfile, name="userprofile_details"),
]