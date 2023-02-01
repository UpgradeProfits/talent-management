from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('seekers')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def authorized_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.category == 'Reader':
            path = request.META['PATH_INFO']
            return redirect(path)
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_user(allowed_roles=[], url=None):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.category:
                group = request.user.category
            if request.user.category is not '':
                for roles in allowed_roles:
                    if group == roles:
                        return view_func(request, *args, **kwargs)
                    else:
                        return redirect(url)
            else:
                return view_func(request, *args, **kwargs)

        return wrapper_func

    return decorator

def one_time_access(view_func):
    def wrapper_function(request, *args, **kwargs):
        check_auth = request.user.authenticated
        if check_auth is True:
            return redirect('seekers')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_function

def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

            if group == 'user':
                return redirect('index')

            if group == 'admin':
                return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('you are not allowed')

    return wrapper_function
