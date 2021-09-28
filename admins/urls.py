
from django.urls import path

app_name = 'admins'

from admins.views import index, UserListView, UserCreateView, UserUpdateView, UserDeleteView
from admins.views import CategoriesListView,  CategoriesCreateView, CategoriesUpdateView, CategoriesDeleteView
from admins.views import ProductsListView, ProductsCreateView, ProductsUpdateView, ProductsDeleteView

urlpatterns = [
   path('', index, name='index'),
   path('users/', UserListView.as_view(), name='admin_users'),
   path('user-create/', UserCreateView.as_view(), name='admin_users_create'),
   path('user-update/<int:pk>', UserUpdateView.as_view(), name='admin_users_update'),
   path('user-delete/<int:pk>', UserDeleteView.as_view(), name='admin_users_delete'),

   path('category/', CategoriesListView.as_view(), name='admin_category'),
   path('category-create/', CategoriesCreateView.as_view(), name='admin_category_create'),
   path('category-update/<int:pk>', CategoriesUpdateView.as_view(), name='admin_category_update'),
   path('category-delete/<int:pk>', CategoriesDeleteView.as_view(), name='admin_category_delete'),

   path('products/', ProductsListView.as_view(), name='admin_products'),
   path('products-create/', ProductsCreateView.as_view(), name='admin_products_create'),
   path('products-update/<int:pk>', ProductsUpdateView.as_view(), name='admin_products_update'),
   path('products-delete/<int:pk>', ProductsDeleteView.as_view(), name='admin_products_delete'),
]
