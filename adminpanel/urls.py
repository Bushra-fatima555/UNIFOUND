
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('claims/', views.manage_claims, name='manage_claims'),

    path(
        'update-claim/<int:claim_id>/',
        views.update_claim_status,
        name='update_claim_status'
    ),
]

