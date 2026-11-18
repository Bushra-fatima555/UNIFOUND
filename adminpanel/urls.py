
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

    path(
        'students/',
        views.manage_students,
        name='manage_students'
    ),
    path(
    'students/<int:student_id>/',
    views.student_detail,
    name='student_detail'
),
path(
    'students/<int:student_id>/toggle-status/',
    views.toggle_student_status,
    name='toggle_student_status'
),
]

