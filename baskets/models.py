from django.db import models
from users.models import User
from products.models import Products


class Basket(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    created_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукты {self.product.name}'


    def sum_product(self):
        # return 1
        return self.quantity * self.product.price


    def sum_quantity(self):
        items = Basket.objects.filter(user=self.user)
        total_quantity = 0
        for i in items:
            total_quantity += i.quantity
        return total_quantity


    def sum_cost(self):
        items = Basket.objects.filter(user=self.user)
        total_cost = 0
        for i in items:
            total_cost += i.sum_product()

        return total_cost
