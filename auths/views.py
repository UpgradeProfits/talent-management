from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from .forms import RegisterForm, UserProfileForm, ClientProfileForm, ExtraFieldForm, SalesOfferForm
from .models import User, Days, UserProfile, ExtraField, Sales_Offer
from .decorators import unauthenticated_user, one_time_access
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
import json
import sys

# sign-up view here ;)
@unauthenticated_user
def sign_up_view(request):
    form= RegisterForm
    if request.method == "POST":
        form= RegisterForm(request.POST or None)
    context = {
        'form': form,
    }
    return render(request, 'sign-up.html', context)
@unauthenticated_user
def sign_up(request):
    if request.method=="POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        create_user= User.objects.create(first_name=firstname, last_name=lastname, email=email)
        create_user.set_password(password)
        create_user.save()
        mssg = f"Account created successfully for {email}"
        # message = f""" Hi {firstname} {lastname} \n welcome to Talent-Mangement, please do verify your account here at http://localhost:8000/ so we can tell you are wonderful person :) \n \n<b>Tech Team</b>"""
        # subject = f'verify account for {email}'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = [email,]
        # send_mail( subject, message, email_from, recipient_list, fail_silently=False)

    return HttpResponse(mssg)

# Log In
@unauthenticated_user
def sign_in_view(request):
    """
    Sign In page staging view
    """
    context= {}
    return render(request, 'login.html', context)
@unauthenticated_user
def sign_in(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        user1 = request.user
        login(request, user)
        if "next" in request.POST:
            return redirect(request.POST.get("next"))
        else:
            return redirect('seekers')
        return HttpResponse('authenticated :)')
    else:
        return HttpResponse('email or password is incorrect')

def log_out(request, user):
    # context={'num':num}
    logout(request)
    return redirect('login')

@one_time_access
@login_required
def user_categories(request):
    context = {}
    return render(request, 'hire_apply.html', context)

@csrf_protect
@ensure_csrf_cookie
@login_required
def createProfile(request):
    # print(request.user)
    form = UserProfileForm
    if request.method == "POST":
        form = UserProfileForm(request.POST or None, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.first_name = request.user.first_name
            instance.last_name = request.user.last_name
            instance.are_you_comfortable_with_commission_based_pay = request.POST.get('commission_selection')
            instance.commission = request.POST.get('commission-num')
            instance.save()
            skills = request.POST.getlist('skills_list')
            days = request.POST.getlist('available_days')
            langs = request.POST.getlist('langs')
            print(f'multiple select fields ; \n skills={skills}, \n days={days}, \n language={langs}')
            skills = [int(j) for e in skills for j in e.split(',')]
            days = [int(j) for e in days for j in e.split(',')]
            langs = [int(j) for e in langs for j in e.split(',')]
            for skill in skills:
                instance.skills.add(skill)
            for lang in langs:
                instance.language.add(lang)
            for day in days:
                instance.days_available.add(day)

            return redirect('details')
        else:
            print(form.errors)
    context = {
        'form': form
    }
    return render(request, 'index.html', context)
@login_required
def update_category(request):
    category = request.POST.get('category')
    value = True
    user = User.objects.filter(id=request.user.pk)
    user.update(category=category, authenticated=value)
    response = 'successfull!!'
    return HttpResponse(response)

@login_required
def updateProfile(request, pk, slug):
    data = UserProfile.objects.get(id=pk)
    form = UserProfileForm(instance=data)
    if request.method == 'POST':
        form = UserProfileForm(request.POST or None, request.FILES, instance=data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            skills = request.POST.getlist('skills_list')
            days = request.POST.getlist('available_days')
            langs = request.POST.getlist('langs')
            print(f'multiple select fields ; \n skills={skills}, \n days={days}, \n language={langs}')
            skills = [int(j) for e in skills for j in e.split(',')]
            days = [int(j) for e in days for j in e.split(',')]
            langs = [int(j) for e in langs for j in e.split(',')]
            for skill in skills:
                instance.skills.add(skill)
            for lang in langs:
                instance.language.add(lang)
            for day in days:
                instance.days_available.add(day)
            return redirect('seekers')
    context = {
        'form':form
    }
    return render(request, 'updateprofile.html', context)
@login_required
def client_profile(request):
    form = ClientProfileForm
    if request.method == 'POST':
        form = ClientProfileForm(request.POST or None, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.full_name = f'{request.user.first_name} {request.user.last_name}'
            instance.save()
            return redirect('seekers')
    context = {
        'form':form
    }
    return render(request, 'index/client-form.html', context)


@csrf_protect
@ensure_csrf_cookie
def other_form(request):
    form=ExtraFieldForm
    if request.method == 'POST':
        form = ExtraFieldForm(request.POST or None)
    context = {
        'form':form,
    }
    return render(request, 'index/first_detail_form_third_page.html', context)


@csrf_protect
@ensure_csrf_cookie
def other_form_ajax(request):
    if request.method == 'POST':
        sales_process = request.POST.get('sales_process')
        leads = request.POST.get('leads')
        past_sales = request.POST.get('past_sales')
        row_data = request.POST.get('row_data')
        last_avg_sales = request.POST.get('last_avg_offer')
        data = json.loads(row_data)
        user = request.user
        new_data = ExtraField.objects.create(
            id=int(request.user.id),
            user=user,
            sales_process=sales_process,
            lead_generation=leads,
            past_sales_training_id=int(past_sales),
            last_avg_sales=last_avg_sales
        )
        saved = new_data.save()

        for i in data:
            # print(i['date'])
            sales_offr = Sales_Offer.objects.create(
                with_field_id = int(request.user.id),
                date=i['date'],
                niche=i['niche'],
                total_generated_rev=i['tot_rev'],
                avg_ticket=i['avg_ticket']
            )
            sales_offr.save()
            redirect('jobs')
    return HttpResponse('Submitted Successfully :)')