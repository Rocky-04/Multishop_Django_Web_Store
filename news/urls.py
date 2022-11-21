from django.urls import path

from .views import *

urlpatterns = [
    path('', NewsView.as_view(), name='news'),
    path('news_category/<str:slug>/', NewsCategoryView.as_view(), name='news_category'),
    path('news_detail/<str:slug>/', NewsDetailView.as_view(), name='news_detail'),
]
