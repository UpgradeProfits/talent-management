from django.shortcuts import render, redirect
from django.db.models import Q
from auths.decorators import allowed_user
from auths.models import UserProfile, Language, ClientProfile
from .forms import AddVacancyForm
from auths.forms import CountryForm, LanguageForm
from django.http import JsonResponse, HttpResponse
from .models import AddVacancy, Apply

# Create your views here.
@allowed_user(allowed_roles=['client'])
def seeker(request):
    query_langs = Language.objects.all()
    form = CountryForm
    obj = Language.objects.all()
    context={
        'langs':query_langs,
        'form': form,
        'obj': obj
    }
    return render(request, 'index/filter.html', context)

def render_data(request):
    if request.method == 'GET':
        query_user_profile = UserProfile.objects.all()[:5]
        return JsonResponse(
            {
                'obj':list(query_user_profile.values())
            }
        )
    if request.method == 'POST':
        pay = request.POST.get('pay')
        category = request.POST.get('category')
        language = request.POST.get('language')
        country = request.POST.get('country')
        print(pay, category, country, language)
        qs = UserProfile.objects.filter(
            Q(pay__icontains=pay) |
            Q(category__icontains=category) |
            Q(language__icontains=language) |
            Q(nationality__icontains=country)
            ).distinct()
        if qs:
            return JsonResponse({
                'results': list(qs.values()),
            })
        else:
            print('No Results for your selection')
            return HttpResponse('No Results for your selection')


def viewProfile(request, slug):
    query_profile = UserProfile.objects.get(slug=slug)
    context = {
        'qs': query_profile,
    }
    return render(request, 'index/profile.html', context)

def create_job(request):
    form = AddVacancyForm
    if request.method == "POST":
        form = AddVacancyForm(request.POST or None, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.status = 'closer'
            instance.save()
            return redirect('seekers')
    context = {
        'form': form,
    }
    return render(request, 'index/post_job.html', context)
@allowed_user(allowed_roles=['seeker'])
def viewJobs(request):
    qs = AddVacancy.objects.all()[:5]
    form = CountryForm
    obj = Language.objects.all()
    context = {
        'qs':qs,
        'form': form,
        'obj': obj
    }
    return render(request, 'filter_job.html', context)

def client(request, str):
    qs = ClientProfile.objects.get(full_name=str)
    context = {
        'qs': qs,
    }
    return render(request, 'index/client_profile.html', context)

def apply(request):
    if request.method == 'POST':
        job = request.POST.get('job')
        link = request.POST.get('link')
        make_apply = Apply.objects.create(
            job=job,
            by=request.user,
            link=link
        )
        make_apply.save()
        return HttpResponse('successfull')