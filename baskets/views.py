from django.db import connection
from django.db.models import F
from django.shortcuts import HttpResponseRedirect
from baskets.models import Basket
from products.models import Products
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def basket_add(request, id):

    product = Products.objects.get(id=id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        baskets = baskets.first()
        # baskets.quantity += 1
        baskets.quantity = F('quantity') + 1
        baskets.save()

        update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
        print(f'basket_add {update_queries}')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, id):
    Basket.objects.get(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        # baskets = Basket.objects.filter(user=request.user)
        # contex = { 'baskets': baskets }
        result = render_to_string('baskets/basket.html', request=request)
        return JsonResponse({'result': result})
