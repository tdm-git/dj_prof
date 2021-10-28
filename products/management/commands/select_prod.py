from django.core.management.base import BaseCommand
from products.models import ProductsCategory, Products
from django.db import connection
from django.db.models import Q
from admins.views import db_profile_by_type

class Command(BaseCommand):
   def handle(self, *args, **options):
       test_products = Products.objects.filter(
           Q(category__name='Новинки') |
           Q(category__name='Распродажа')
       )
       print(test_products)
       # print(len(test_products))
       db_profile_by_type('learn db', '', connection.queries)