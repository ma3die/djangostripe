from django.contrib import admin
from .models import Order, OrderItem
from store.models import Discount, Tax


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['item']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Discount)
admin.site.register(Tax)
