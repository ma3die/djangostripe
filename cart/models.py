from django.db import models
from django.contrib.auth.models import User
from store.models import Item

class Cart(models.Model):
    '''Корзина с товарами'''
    cart_id = models.CharField(max_length=250, blank=True, verbose_name='ID корзины')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return self.cart_id

    class Meta:
        verbose_name = 'Корзину'
        verbose_name_plural = 'Корзины'

class CartItem(models.Model):
    '''Товар хранимый в корзине'''
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Товар')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, verbose_name='Корзина')
    quantity = models.IntegerField(verbose_name='Количество')
    is_active = models.BooleanField(default=True, verbose_name='Активно')

    def sub_total(self):
        return self.item.price * self.quantity

    def __unicode__(self):
        return self.item

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
