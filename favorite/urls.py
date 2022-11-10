from django.urls import path

from .views import FavoriteAddView
from .views import FavoriteRemoveView
from .views import FavotiteView

urlpatterns = [
    path('add/<id>/', view=FavoriteAddView.as_view(), name='add_favorite'),
    path('remove/<id>/', view=FavoriteRemoveView.as_view(),
         name='remove_favorite'),
    path('', FavotiteView.as_view(), name='favorite'),
]
