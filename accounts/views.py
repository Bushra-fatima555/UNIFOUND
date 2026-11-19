
from django.shortcuts import render


def landing(request):
    return render(request, "landing.html")


def student_login(request):
    return render(request, "student_login.html")


def student_signup(request):
    return render(request, "student_signup.html")


def admin_login(request):
    return render(request, "admin_login.html")


def admin_signup(request):
    return render(request, "admin_signup.html")
