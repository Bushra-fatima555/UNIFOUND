from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('claims/', include('claims.urls')),
    path('admin-dashboard/', include('adminpanel.urls')),
    path('lostfound/', include('lostfound.urls')),
]
