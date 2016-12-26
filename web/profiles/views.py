from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.crypto import constant_time_compare

from .forms import SignupForm
from .models import Profile
from .utils import get_activation_hash, send_activation_email


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
                User.objects.create_user(fields['username'], fields['email'], fields['password'], is_active=False)
            except IntegrityError:
                form.add_error('username', 'Пользователь с таким именем уже существует')
            else:
                send_activation_email(request, fields['username'], fields['email'])

                messages.success(request, 'Ссылка для активации аккаунта отправлена на {}'.format(fields['email']))
                return redirect('login')
    else:
        form = SignupForm()

    return render(request, 'profiles/signup.html', {
        'form': form,
        'next': request.GET.get('next', settings.LOGIN_REDIRECT_URL),
    })


def activate(request, username):
    if constant_time_compare(request.GET.get('hash', ''), get_activation_hash(username)):
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()

        messages.success(request, 'Аккаунт {} активирован, теперь можно войти на сайт'.format(username))
    else:
        messages.error(request, 'Это ссылка не подходит для активации аккаунта {}'.format(username))
    return redirect('login')
