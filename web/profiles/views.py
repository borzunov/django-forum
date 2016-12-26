from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from .forms import SignupForm
from .models import Profile


def show(request, username):
    profile = get_object_or_404(Profile, username=username)

    return render(request, 'profiles/show.html', {
        'profile': profile,
    })


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            fields = form.cleaned_data
            try:
                User.objects.create_user(fields['username'], fields['email'], fields['password'])
            except IntegrityError:
                form.add_error('username', 'Пользователь с таким именем уже существует')
            else:
                user = authenticate(username=fields['username'], password=fields['password'])
                login(request, user)

                return HttpResponseRedirect(request.POST.get('next', settings.LOGIN_REDIRECT_URL))
    else:
        form = SignupForm()

    return render(request, 'profiles/signup.html', {
        'form': form,
        'next': request.GET.get('next', settings.LOGIN_REDIRECT_URL),
    })
