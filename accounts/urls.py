
from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),

    path("student/login/", views.student_login, name="student_login"),
    path("student/signup/", views.student_signup, name="student_signup"),

    path("admin/login/", views.admin_login, name="admin_login"),
    path("admin/signup/", views.admin_signup, name="admin_signup"),
]
