from django.urls import path
from . import views


urlpatterns = [
    path('created_order/', views.order_create, name='order-create'),

]