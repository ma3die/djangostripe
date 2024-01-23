# Generated by Django 5.0 on 2024-01-16 13:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
        ('store', '0003_discount_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='store.discount', verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='store.tax', verbose_name='Налог'),
        ),
    ]