from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import RegisterForm
from .models import User

# sign-up view here ;)
def sign_up(request):
    form= RegisterForm
    if request.method == "POST":
        form= RegisterForm(request.POST or None)
    context = {
        'form': form,
    }
    return render(request, 'index.html', context)

def get_details(request):
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

def user_categories(request):
    context = {}
    return render(request, 'hire_apply.html', context)