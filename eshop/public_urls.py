# eshop/public_urls.py

from django.urls import path,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from base.views import HomeView
from django.http import HttpResponse
def HomeView(request):
    return HttpResponse('hello world')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView, name="home"),
    path("accounts/", include("base.urls")),
    path('auth/', include('allauth.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)