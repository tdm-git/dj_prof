from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy

from geekshop import settings
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
            user = form.save()
            if send_verify_mail(user):
                messages.success(request,'Вы успешно зарегистрировались на сайте')
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


def send_verify_mail(user):
    verify_link = reverse('users:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} перейдите по ссылке: \n {settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.activation_key = ''
            user.activation_key_expires = None
            user.is_active = True
            user.save()
            auth.login(request, user)
        return render(request, 'users/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))
