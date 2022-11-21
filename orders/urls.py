from django.urls import path

from .views import *

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout/create_order/', CreateOrderView.as_view(), name='create_order'),
]
