from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, UserProfileForm
from .models import User, Days
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

def createProfile(request):
    print(request.user)
    form = UserProfileForm
    if request.method == "POST":
        form = UserProfileForm(request.POST or None, request.FILES)
        if form.is_valid():
            skills = request.POST.get('skills_list')
            days_available = request.POST.get('available_days')
            language = request.POST.get('langs')
            print(f'multiple select fields ; \n skills={skills}, \n days={days_available}, \n language={language}')
            # skills = [int(j) for e in skills for j in e.split(',')]
            # days_available = [int(j) for e in days_available for j in e.split(',')]
            # language = [int(j) for e in language for j in e.split(',')]
            instance = form.save(commit=False)
            instance.user = request.user
            # instance.user = request.user
            # instance.user = request.user
            instance.save()
    context = {
        'form': form
    }
    return render(request, 'userprofile.html', context)

def userProfile(request):
    pass