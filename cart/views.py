from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from cart.models import Cart, CartItem
from store.models import Item


def cart_id(request):
    '''Получение корзины по ключу session_key в сеансе'''
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, item_id):
    '''Добавление товара в корзину'''
    current_user = request.user
    item = Item.objects.get(id=item_id)  # get the product
    if current_user.is_authenticated:
        cart_item = CartItem.objects.create(item=item, quantity=1, user=current_user)
        cart_item.save()
    else:
        try:
            cart = Cart.objects.get(cart_id=cart_id(request))
        except ObjectDoesNotExist:
            cart = Cart.objects.create(cart_id=cart_id(request))
            cart.save()
        is_cart_item_exists = CartItem.objects.filter(item_id=item_id, cart=cart).exists()
        if not is_cart_item_exists:
            cart_item = CartItem.objects.create(item=item, quantity=1, cart=cart)
            cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_page(request, total=0, cart_items=None):
    '''Отображение корзины'''
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.item.price * cart_item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'cart_items': cart_items,
    }

    return render(request, 'items/cart.html', context)


def remove_cart_item(request, item_id, cart_item_id):
    '''Удаление товара из корзины'''
    item = get_object_or_404(Item, id=item_id)
    cart = Cart.objects.get(cart_id=cart_id(request))
    cart_item = CartItem.objects.get(item=item, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def checkout(request, total=0, quantity=0, cart_items=None,):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.item.price * cart_item.quantity
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'orders/create_order.html', context)
