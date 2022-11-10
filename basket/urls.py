from django.urls import path

from .views import *

urlpatterns = [
    path('', view=ViewCart.as_view(), name='basket'),
    path('add_basket/<id>/', view=BasketAddView.as_view(), name='add_basket'),
    path('remove_basket/<id>/', view=BasketRemoveView.as_view(),
         name='remove_basket'),
    path('edit_basket/<id>/', view=EditCartView.as_view(), name='edit_basket'),

]
