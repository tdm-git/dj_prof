from django.db import models
from users.models import User
from products.models import Products
from django.utils.functional import cached_property


# class BasketQuerySet(models.QuerySet):
#
#    def delete(self, *args, **kwargs):
#        for object in self:
#            object.product.quantity += object.quantity
#            object.product.save()
#        super(BasketQuerySet, self).delete(*args, **kwargs)

class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    created_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукты {self.product.name}'

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()


    def sum_product(self):
        # return 1
        return self.quantity * self.product.price


    def sum_quantity(self):
        # items = Basket.objects.filter(user=self.user)
        items = self.get_items_cached
        total_quantity = 0
        for i in items:
            total_quantity += i.quantity
        return total_quantity


    def sum_cost(self):
        # items = Basket.objects.filter(user=self.user)
        items = self.get_items_cached
        total_cost = 0
        for i in items:
            total_cost += i.sum_product()

        return total_cost

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)

    # def delete(self, *args, **kwargs):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(Basket, self).delete(*args, **kwargs)
    #
    # # переопределяем метод, сохранения объекта
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(self.__class__, self).save(*args, **kwargs)