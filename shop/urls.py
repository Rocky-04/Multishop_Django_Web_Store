from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('detail/<str:slug>/', ProductDetailView.as_view(), name='detail'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('category/<str:slug>/', CategoryView.as_view(), name='category'),
    path('tag/<str:slug>/', TagView.as_view(), name='tag'),
    path('brand/<str:slug>/', BrandView.as_view(), name='brand'),
    path('about-us/', AboutView.as_view(), name='about'),
    path('help/', HelpView.as_view(), name='help'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('search/', SearchView.as_view(), name='search'),
    path('filter/', view=FilterView.as_view(), name='filter'),
    path('skip_filter/', view=SkipFilterView.as_view(), name='skip_filter'),
    path('add_review/', AddReviewView.as_view(), name='add_review'),
    path('send_user_mail', SendUserMailView.as_view(), name='send_user_mail'),
]
