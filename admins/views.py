from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse,reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

from users.models import User
from products.models import ProductsCategory, Products
from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, CategoryAdminForm, ProductsAdminForm


def index(request):
    return render(request, 'admins/admin.html')


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users(request):
#     context = {
#         'users': User.objects.all(),
#     }
#     return render(request, 'admins/admin-users-read.html', context)
class UserListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'admins/admin-users-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
#
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admins:admin_users'))
#     else:
#         form = UserAdminRegisterForm()
#     context = {
#         'title': 'Регистрация',
#         'form': form
#     }
#     return render(request, 'admins/admin-users-create.html', context)
class UserCreateView(CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admin_users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request, id):
#     user_select = User.objects.get(id=id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST, instance=user_select, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admins:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance=user_select)
#     context = {
#         'title': 'Профиль',
#         'user_select': user_select,
#         'form': form
#     }
#     return render(request, 'admins/admin-users-update-delete.html', context)
class UserUpdateView(UpdateView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admin_users')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Обновление пользователя'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_delete(request, id):
#     user_select = User.objects.get(id=id)
#     user_select.is_active = False
#     user_select.save()
#     # user_select.delete()
#     return HttpResponseRedirect(reverse('admins:admin_users'))
class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

 # CATEGORIES

class CategoriesListView(ListView):
    model = ProductsCategory
    context_object_name = 'categories'
    template_name = 'admins/admin-category-list.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoriesListView, self).dispatch(request, *args, **kwargs)


class CategoriesCreateView(CreateView):
    model = ProductsCategory
    template_name = 'admins/admin-category-create.html'
    form_class = CategoryAdminForm
    success_url = reverse_lazy('admins:admin_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriesCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Новая категория'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoriesCreateView, self).dispatch(request, *args, **kwargs)


class CategoriesUpdateView(UpdateView):
    model = ProductsCategory
    template_name = 'admins/admin-category-update-delete.html'
    form_class = CategoryAdminForm
    success_url = reverse_lazy('admins:admin_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriesUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Обновление категории'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoriesUpdateView, self).dispatch(request, *args, **kwargs)


class CategoriesDeleteView(DeleteView):
    model = ProductsCategory
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admin_category')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoriesDeleteView, self).dispatch(request, *args, **kwargs)

# PRODUCTS

class ProductsListView(ListView):
    model = Products
    context_object_name = 'products'
    template_name = 'admins/admin-products-list.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductsListView, self).dispatch(request, *args, **kwargs)


class ProductsCreateView(CreateView):
    model = Products
    template_name = 'admins/admin-products-create.html'
    form_class = ProductsAdminForm
    success_url = reverse_lazy('admins:admin_products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Новая товар'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductsCreateView, self).dispatch(request, *args, **kwargs)


class ProductsUpdateView(UpdateView):
    model = Products
    template_name = 'admins/admin-products-update-delete.html'
    form_class = ProductsAdminForm
    success_url = reverse_lazy('admins:admin_products')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Изменение товара'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductsUpdateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_products_delete(request, id):
#     product_select = Products.objects.get(id=id)
#     product_select.delete()
#     return HttpResponseRedirect(reverse('admins:admin_products'))
class ProductsDeleteView(DeleteView):
    model = Products
    template_name = 'admins/admin-products-update-delete.html'
    success_url = reverse_lazy('admins:admin_products')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductsDeleteView, self).dispatch(request, *args, **kwargs)