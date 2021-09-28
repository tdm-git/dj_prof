from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import ProductsCategory, Products
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.
# Контроллер функции
def index(request):
    context = {'title': 'Главная',
               'curr_date': date.today()}

    return render(request, 'products/index.html', context)


def products(request, id=None, page=1):
    products = Products.objects.filter(category_id=id) if id != None else Products.objects.all()
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