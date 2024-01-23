import stripe
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.conf import settings
from django.http import JsonResponse
from .models import Item
from orders.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemListView(ListView):
    '''View для каталога товаров'''
    model = Item
    context_object_name = 'items'
    template_name = 'items/item_list.html'


class ItemDetailView(DetailView):
    '''View для детальной старницы товара'''
    model = Item
    context_object_name = 'item'
    template_name = 'items/item.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data()
        context.update({'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})
        return context


class CreateCheckoutSessionView(View):
    '''View для оплаты одного товара через Stripe'''
    def post(self, request, *args, **kwargs):
        item_id = kwargs['pk']
        item = get_object_or_404(Item, id=item_id)
        domain = 'http://127.0.0.1:7775'
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'rub',
                            'unit_amount_decimal': item.price_unit,
                            'product_data': {'name': item.name}
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=domain + '/success/',
                cancel_url=domain + '/cancel/'
            )
            return JsonResponse({
                'id': checkout_session.id
            })
        except Exception as err:
            print(err)


class CreateOrderCheckoutSessionView(View):
    '''View для оплаты нескольких товаров в корзине через Stripe'''
    def post(self, request, *args, **kwargs):
        order_id = kwargs['pk']
        domain = 'http://127.0.0.1:7775'
        try:
            order = get_object_or_404(Order, id=order_id)
            order_items = OrderItem.objects.filter(order_id=order_id)
            data = []
            for item in order_items:
                total = item.item.price
                data_el = {
                    'price_data': {
                        'currency': 'rub',
                        'unit_amount_decimal': item.item.price_unit,
                        'product_data': {'name': item.item.name}
                    },
                    'quantity': 1,
                }
                if order.discount:
                    discount_sum = total * order.discount.percent // 100
                    total_discount = total - discount_sum
                    data_el['price_data']['unit_amount_decimal'] = total_discount * 100
                data.append(data_el)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=data,
                mode='payment',
                success_url=domain + '/success/',
                cancel_url=domain + '/cancel/'
            )
            return JsonResponse({
                'id': checkout_session.id
            })
        except Exception as err:
            print(err)


class SuccessView(TemplateView):
    '''View успешной оплаты через Stripe'''
    template_name = 'items/success.html'


class CancelView(TemplateView):
    '''View не успешной оплаты через Stripe'''
    template_name = "items/cancel.html"
