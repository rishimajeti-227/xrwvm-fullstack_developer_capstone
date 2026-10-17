from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    # redirect root to djangoapp
    path('', lambda request: redirect('djangoapp:index')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
