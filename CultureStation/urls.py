from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('admin/', admin.site.urls),
    path('get-response/', views.get_response),
    path('shop/', include('shop.urls')),
    path('dashboard/', include('dashboard.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
