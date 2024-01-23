from django.db import models
from django.contrib.auth.models import User
from store.models import Item, Discount, Tax

class Order(models.Model):
    '''Заказ'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Почта')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    paid = models.BooleanField(default=False, verbose_name='Заказан')
    discount = models.ForeignKey(Discount, on_delete=models.SET_DEFAULT, null=True, default=None, verbose_name='Скидка')
    tax = models.ForeignKey(Tax, on_delete=models.SET_DEFAULT, null=True, default=None, verbose_name='Налог')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def full_name(self):
        return f'{self.last_name} {self.first_name}'

    def __str__(self):
        return str(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    '''Товары в заказе'''
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
