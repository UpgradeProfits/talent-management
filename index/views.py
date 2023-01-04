from django.shortcuts import render
from auths.models import UserProfile

# Create your views here.
def index(request):
    query_obj = UserProfile.objects.all()[:5]
    context = {
        'obj':query_obj
    }
    return render(request, 'index/filter.html', context)