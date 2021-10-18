from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date

from django.views.generic import FormView

from .models import ProductsCategory, Products
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.
# Контроллер функции
def index(request):
    context = {'title': 'Главная',
               'curr_date': date.today()}#
    return render(request, 'products/index.html', context)


def products(request, id=None, page=1):
    products = Products.objects.filter(category_id=id).select_related('category') if id != None else Products.objects.all().select_related('category')
    paginator = Paginator(products, per_page=3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    content = {'title': 'Каталог',
               'curr_date': date.today(),
               'categories': ProductsCategory.objects.all(),
               'products': products_paginator,  # Products.objects.all()
              }

    return render(request, 'products/products.html', content)
# class ProductsFormView(FormView):
#     model = Products
#     context_object_name = 'products'
#     template_name = 'products/products.html'
#     # form_class = UserRegisterForm
#     # success_url = reverse_lazy('users:login')
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductsFormView, self).get_context_data(**kwargs)
#         context['title'] = 'Каталог'
#         context['curr_date'] = 'date.today()'
#         context['categories'] = ProductsCategory.objects.all()
#         context['products_paginator'] = Paginator(Products.objects.all(), per_page=3)
#         return context