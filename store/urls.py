from django.urls import path
from .views import ItemListView, ItemDetailView, CreateCheckoutSessionView, SuccessView, CancelView
from .views import CreateOrderCheckoutSessionView
urlpatterns = [
    path('', ItemListView.as_view(), name='item-list'),
    path('item/<int:pk>', ItemDetailView.as_view(), name='item'),
    path('buy/<int:pk>', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('created_order/<int:pk>/', CreateOrderCheckoutSessionView.as_view(), name='create-order-checkout-session'),
    path('success/', SuccessView.as_view()),
    path('cancel/', CancelView.as_view()),

]