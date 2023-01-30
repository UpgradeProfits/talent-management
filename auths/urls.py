from django.urls import path
from auths import views

urlpatterns = [
    # SignUp urls
    path('signup/', views.sign_up_view, name="sign-up"),
    path('user/', views.sign_up),#this is the url that ajax sends the users detail to for authentication @ the sign_up view
    # SignIn urls
    path('signin/', views.sign_in_view, name="login"),
    path('login/', views.sign_in),#this is the url that ajax sends the users detail to for authentication @ the sign_in view
    # SignOut
    path('signout/<str:user>/', views.log_out, name="logout"),
    #Reset Password url
    # path('password_reset/', django_views.PasswordResetView.as_view(), name="reset_password"),
    #
    path('category/', views.user_categories, name='category'),
    path('update/', views.update_category, name='category_update'),
    path('createprofile/', views.createProfile, name="c_profile"),
    path('createprofile/client/', views.client_profile, name="client_profile"),
    path('updateprofile/<int:pk>/<slug:slug>/', views.updateProfile, name="updateprofile"),
]