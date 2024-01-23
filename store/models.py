from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Item(models.Model):
    '''Товары'''
    name = models.CharField(max_length=100, verbose_name='Наименование товара')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='product_images/', verbose_name='Фото товара')

    def __str__(self):
        return self.name

    @property
    def price_unit(self):
        return int(self.price * 100)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Discount(models.Model):
    '''Скидка'''
    name = models.CharField(max_length=30, unique=True, verbose_name='Скидка')
    percent = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)], verbose_name='Процент')

    def __str__(self):
        return str(self.name) + '-' + f'{self.percent}%'

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Tax(models.Model):
    '''Налог'''
    name = models.CharField(max_length=30, unique=True, verbose_name='Налог')
    value = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)], verbose_name='Процент')

    def __str__(self):
        return str(self.name) + '-' + f'{self.value}%'

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'