from django.contrib import admin
from django.urls import path, include

app_name = 'baskets'

from .views import basket_add, basket_remove, basket_edit

urlpatterns = [
   path('basket_add/<int:id>', basket_add, name='basket_add'),
   path('delete/<int:id>', basket_remove, name='basket_remove'),
   path('edit/<int:id>/<int:quantity>/', basket_edit, name='basket_edit'),
]