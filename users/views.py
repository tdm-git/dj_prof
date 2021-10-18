from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView, UpdateView

from geekshop import settings
from .models import User
from datetime import date
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from baskets.models import Basket



# Create your views here.
# Контроллер функции
# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#             # else:
#             #     print(form.errors)
#     else:
#         form = UserLoginForm()
#     context = {
#         'title': 'Авторизация',
#         'form': form
#     }
#     return render(request, 'users/login.html', context)
class LoginListView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super(LoginListView, self).get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             if send_verify_mail(user):
#                 messages.success(request,'Вы успешно зарегистрировались на сайте')
#             return HttpResponseRedirect(reverse('users:login'))
#         # else:
#         #     print(form.errors)
#     else:
#         form = UserRegisterForm()
#     context = {
#         'title': 'Регистрация',
#         'form': form
#     }#
#     return render(request, 'users/register.html', context)
class RegisterFormView(SuccessMessageMixin, FormView):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрировались на сайте'

    def get_context_data(self, **kwargs):
        context = super(RegisterFormView, self).get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.success(request,'Вы успешно зарегистрировались на сайте')
                # return HttpResponseRedirect(reverse('users:login'))
                return redirect(self.success_url)
            return redirect(self.success_url)

        return render(request, self.template_name, {'from': form})

    @staticmethod
    def send_verify_link(user):
        verify_link = reverse('users:verify', args=[user.email, user.activation_key])
        title = f'Подтверждение учетной записи {user.username}'
        message = f'Для подтверждения учетной записи {user.username} перейдите по ссылке: \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    @staticmethod
    def verify(request, email, activation_key):
        try:
            user = User.objects.get(email=email)
            if user.activation_key == activation_key and not user.is_activation_key_expired():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'users/verification.html')
        except Exception as e:
            print(f'error activation user : {e.args}')
            return HttpResponseRedirect(reverse('index'))



# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
#         if form.is_valid() and profile_form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#         profile_form = UserProfileEditForm(instance=request.user.userprofile)
#
#     context = {
#         'title': 'Профиль',
#         'curr_date': date.today(),
#         # 'baskets': Basket.objects.filter(user=request.user),
#         'form': form,
#         'profile_form': profile_form,
#     }
#     return render(request, 'users/profile.html', context)
class ProfileFormView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    form_class_second = UserProfileEditForm

    def get_context_data(self, **kwargs):
        context = super(ProfileFormView, self).get_context_data(**kwargs)
        context['title'] = 'Профиль'
        context['profile_form'] = UserProfileEditForm(instance=self.request.user.userprofile)

        return context

    def get_object(self, *args, **kwargs):
        return get_object_or_404(User, pk=self.request.user.pk)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        edit_form = UserProfileForm(data=request.POST, instance=user, files=request.FILES)
        profile_form = UserProfileEditForm(data=request.POST, instance=user.userprofile, files=request.FILES)
        if edit_form.is_valid() and profile_form.is_valid():
                edit_form.save()
                return HttpResponseRedirect(self.success_url)

        return render(request, self.template_name, {
            'form': edit_form,
            'profile_form': profile_form,
        })


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))
class Logout(LogoutView):
    template_name = 'products/index.html'


# def send_verify_mail(user):
#     verify_link = reverse('users:verify', args=[user.email, user.activation_key])
#     title = f'Подтверждение учетной записи {user.username}'
#     message = f'Для подтверждения учетной записи {user.username} перейдите по ссылке: \n {settings.DOMAIN_NAME}{verify_link}'
#
#     return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


# def verify(request, email, activation_key):
#     try:
#         user = User.objects.get(email=email)
#         if user.activation_key == activation_key and not user.is_activation_key_expired():
#             user.activation_key = ''
#             user.activation_key_expires = None
#             user.is_active = True
#             user.save()
#             # auth.login(request, user)
#             auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#         return render(request, 'users/verification.html')
#     except Exception as e:
#         print(f'error activation user : {e.args}')
#         return HttpResponseRedirect(reverse('index'))
