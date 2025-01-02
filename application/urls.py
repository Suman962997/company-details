from django.urls import path
from .views import webscraping
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('webscraping/',webscraping.as_view(),name='webscraping')
]#+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)