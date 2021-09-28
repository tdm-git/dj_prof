from django.contrib import admin
from .models import ProductsCategory, Products

# Register your models here.

admin.site.register(ProductsCategory)
# admin.site.register(Products)
@admin.register(Products)
class Product(admin.ModelAdmin):

    list_display = ('name','price','quantity','category')
    fields = ('name','image','description',('price','quantity'),'category')
    readonly_fields = ('description',)
    ordering = ('name','price')
    search_fields = ('name',)