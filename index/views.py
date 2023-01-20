from django.shortcuts import render, redirect
from django.db.models import Q
from auths.models import UserProfile, Language
from .forms import AddVacancyForm
from auths.forms import CountryForm
from django.http import JsonResponse, HttpResponse
from .models import AddVacancy

# Create your views here.
def index(request):
    query_langs = Language.objects.all()
    form = CountryForm
    context={
        'langs':query_langs,
        'form': form
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
    elif request.method == 'POST':
        pay = request.POST.get('pay')
        category = request.POST.get('category')
        country = request.POST.get('country')
        print(pay, category, country)
        qs = UserProfile.objects.filter(
            Q(pay__icontains=pay) |
            Q(category__icontains=category) |
            Q(nationality__icontains=country)
            ).distinct()
        if qs:
            return JsonResponse({
                'results': list(qs.values()),
            })
        else:
            print('No Results for your selection')
            return HttpResponse('No Results for your selection')


def viewProfile(request, pk, slug):
    query_profile = UserProfile.objects.get(id=pk)
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
            return redirect('/')
    context = {
        'form': form,
    }
    return render(request, 'index/post_job.html', context)

def viewJobs(request):
    qs = AddVacancy.objects.all()[:5]
    context = {
        'qs':qs
    }
    return render(request, 'filter_job.html', context)