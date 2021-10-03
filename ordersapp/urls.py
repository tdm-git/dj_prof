from django.contrib import admin
from django.urls import path, include

app_name = 'ordersapp'

from .views import OrderList, OrderCreate, OrderUpdate, OrderDelete, OrderDetail, order_forming_complete

urlpatterns = [
    path('', OrderList.as_view(), name='list'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('read/<int:pk>', OrderDetail.as_view(), name='read'),
    path('update/<int:pk>', OrderUpdate.as_view(), name='update'),
    path('delete/<int:pk>', OrderDelete.as_view(), name='delete'),
    path('forming-complite/<int:pk>/', order_forming_complete, name='forming_complete'),
]