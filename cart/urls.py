from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_page, name='cart'),
    path('add_cart/<int:item_id>/', views.add_cart, name='add_cart'),
    path('remove_cart_item/<int:item_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('create_order/', views.checkout, name='checkout'),
]