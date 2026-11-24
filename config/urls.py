
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # Claims Module
    path("claims/", include("claims.urls")),

    # Admin Dashboard
    path("admin-dashboard/", include("adminpanel.urls")),

    # Accounts Module
    path("", include("accounts.urls")),

    # Lost & Found Module
    path("lostfound/", include("lostfound.urls")),
]

# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
