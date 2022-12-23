from django.shortcuts import render

# sign-up view here ;)
def sign_up(request):
    context = {}
    return render(request, 'index.html', context)