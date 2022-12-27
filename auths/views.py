from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from .models import User
import json

# sign-up view here ;)
def sign_up_view(request):
    form= RegisterForm
    if request.method == "POST":
        form= RegisterForm(request.POST or None)
    context = {
        'form': form,
    }
    return render(request, 'sign-up.html', context)

def sign_up(request):
    if request.method=="POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        password = request.POST.get('password')

        create_user= User.objects.create(first_name=firstname, last_name=lastname, email=email, tel=tel)
        create_user.set_password(password)
        create_user.save()
        mssg = f'Account created for {firstname}'

    return HttpResponse(mssg)

# Log In
def sign_in_view(request):
    """
    Sign In page staging view 
    """
    context= {}
    return render(request, 'login.html', context)

def sign_in(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        user1 = request.user
        login(request, user)
        # if "next" in request.POST:
        #     return redirect(request.POST.get("next"))
        # else:
        #     return redirect('home')
        return HttpResponse('authenticated')
    else:
        return HttpResponse('email or password is incorrect')


def log_out(request, pk='first_name'):
    # context={'num':num}
    logout(request)
    return redirect('login')
def user_categories(request):
    context = {}
    return render(request, 'hire_apply.html', context)