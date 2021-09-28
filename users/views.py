from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from .models import User
from datetime import date
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm
from baskets.models import Basket


# Create your views here.
# Контроллер функции
def login(request):
    if request.method == 'POST':

        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
            # else:
            #     print(form.errors)
    else:
        form = UserLoginForm()
    context = {
        'title': 'Авторизация',
        'form': form
    }

    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Вы зарегистрировались на сайте')
            return HttpResponseRedirect(reverse('users:login'))
        # else:
        #     print(form.errors)
    else:
        form = UserRegisterForm()
    context = {
        'title': 'Регистрация',
        'form': form
    }

    return render(request, 'users/register.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'title': 'Профиль',
        'curr_date': date.today(),
        'baskets': Basket.objects.filter(user=request.user),
        'form': form
    }

    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)

    return HttpResponseRedirect(reverse('index'))
