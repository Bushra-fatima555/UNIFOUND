from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # Claims Module
    path("claims/", include("claims.urls")),

    # Admin Dashboard
    path("admin-dashboard/", include("adminpanel.urls")),

    # Accounts Module
    path("", include("accounts.urls")),
]
