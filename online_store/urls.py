from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.static import serve as mediaserve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18h/', include('django.conf.urls.i18n')),
    path('captcha/', include('captcha.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

urlpatterns += i18n_patterns(
    path('', include('shop.urls')),
    path('news/', include('news.urls')),
    path('order/', include('orders.urls')),
    path('user/', include('users.urls')),
    path('favorite/', include('favorite.urls')),
    path('basket/', include('basket.urls')),
)

if settings.DEBUG:
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(f'^{settings.MEDIA_URL.lstrip("/")}(?P<path>.*)$',
                mediaserve, {'document_root': settings.MEDIA_ROOT}),
        re_path(f'^{settings.STATIC_URL.lstrip("/")}(?P<path>.*)$',
                mediaserve, {'document_root': settings.STATIC_ROOT}),
    ]

handler404 = 'shop.views.custom_page_not_found_view'
handler500 = 'shop.views.custom_page_server_error'
