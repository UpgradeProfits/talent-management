from django.urls import path
from index import views
from auths import views as auth_views

urlpatterns = [
    path('', auth_views.sign_up_view, name="sign-up"),
    path('seekers/', views.seeker, name="seekers"),
    path('render_data/', views.render_data, name="render_data"),
    path('userprofile/<int:pk>/<slug:slug>/', views.viewProfile, name='u-profile'),
    path('clientprofile/<str:str>/', views.client, name='c-profile'),
    path('jobs/', views.viewJobs, name='jobs'),
    path('add_job/', views.create_job, name='add_job'),
    path('apply/', views.apply, name='apply')
]