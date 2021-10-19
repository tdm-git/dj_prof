from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date

from django.views.generic import FormView, DetailView

from .models import ProductsCategory, Products
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.conf import settings
from django.core.cache import cache

# Create your views here.
# Контроллер функции
def get_links_category():
   if settings.LOW_CACHE:
       key = 'links_category'
       links_category = cache.get(key)
       if links_category is None:
           links_category = ProductsCategory.objects.filter(is_active=True)
           cache.set(key, links_category)
       return links_category
   else:
       return ProductsCategory.objects.filter(is_active=True)


def get_links_products():
   if settings.LOW_CACHE:
       key = 'links_products'
       links_products = cache.get(key)
       if links_products is None:
           links_products = Products.objects.filter(is_active=True, category__is_active=True).select_related('category')
           cache.set(key, links_products)
       return links_products
   else:
       return Products.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
   if settings.LOW_CACHE:
       key = f'product_{pk}'
       product = cache.get(key)
       if product is None:
           product = get_object_or_404(Products, pk=pk)
           cache.set(key, product)
       return product
   else:
       return get_object_or_404(Products, pk=pk)


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
               'categories': get_links_category(),
               # 'categories': ProductsCategory.objects.all(),
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


class ProductDetail(DetailView):
    model = Products
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, category_id=None, *args, **kwargs):
        context = super().get_context_data()
        context['product'] = get_product(self.kwargs.get('pk'))
        context['categories'] = ProductsCategory.objects.all()
        return context