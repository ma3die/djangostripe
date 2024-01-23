import random
import string
from django.shortcuts import render, redirect
from .models import OrderItem, Discount, Tax
from django.conf import settings
from .forms import OrderCreateForm
from django.contrib.auth.models import User
from store.models import Discount, Tax
from cart.views import Cart, CartItem, cart_id


def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))


def get_user(user):
    '''Функция для заполнения данных для анонимного пользователя'''
    if user.is_anonymous:
        random_username = f"{randomString(10)}_guest"
        random_email = f"{randomString(5)}_guest@example.com"
        guest_user = User.objects.create(username=random_username, is_active=False, email=random_email)
        return guest_user
    else:
        pass


def order_create(request, total=0, total_discount=0):
    '''Создание заказаз'''
    user = request.user
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=user, is_active=True)
    else:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        if user.is_anonymous:
            user = get_user(user)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user
            order = form.save()
            for it in cart_items:
                OrderItem.objects.create(order=order,
                                         item=it.item,
                                         price=it.item.price,
                                         quantity=it.quantity)
            order_items = OrderItem.objects.filter(order_id=order.id)
            # очистка корзины
            for cart_item in cart_items:
                total += cart_item.item.price * cart_item.quantity
                cart_item.delete()
            if not request.user.is_authenticated:
                cart.delete()
            if total > 100000:
                discount = Discount.objects.get(name='Скидка')
                order.discount_id = discount.id
                order.save()
                discount_sum = total * order.discount.percent // 100
                total_discount = total - discount_sum
            context = {
                'order': order,
                'order_items': order_items,
                'total': total,
                'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
            }
            if total_discount:
                context['total_discount'] = total_discount
                context['discount_sum'] = discount_sum
            return render(request, 'orders/created_order.html', context)
    else:
        return redirect('checkout')
