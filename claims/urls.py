from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_claim, name='submit_claim'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
]
