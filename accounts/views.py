
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.db import transaction
from django.db import IntegrityError

from .models import StudentProfile


def landing(request):
    return render(request, 'landing.html')


def signup(request):

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')
        return redirect('item_list')

    if request.method == 'POST':

        full_name = request.POST.get('full_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        roll_number = request.POST.get('roll_number', '').strip()
        department = request.POST.get('department', '').strip()
        semester = request.POST.get('semester', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get(
            'confirm_password',
            request.POST.get('password2', '')
        )

        if not username:
            username = roll_number

        if not all([
            full_name, username, roll_number,
            department, semester, password, confirm_password
        ]):
            messages.error(request, 'Please fill in all required fields.')

        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')

        elif len(password) < 8:
            messages.error(request, 'Password must contain at least 8 characters.')

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')

        elif User.objects.filter(email=email).exists() and email:
            messages.error(request, 'Email already exists.')

        elif StudentProfile.objects.filter(
            roll_number=roll_number
        ).exists():
            messages.error(request, 'Roll number already registered.')

        elif department not in dict(StudentProfile.DEPARTMENT_CHOICES):
            messages.error(request, 'Please select a valid department.')

        elif not semester.isdigit() or int(semester) not in dict(
            StudentProfile.SEMESTER_CHOICES
        ):
            messages.error(request, 'Please select a valid semester.')

        else:
            try:
                with transaction.atomic():

                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password,
                        first_name=full_name,
                        is_staff=False,
                        is_superuser=False
                    )

                    StudentProfile.objects.create(
                        user=user,
                        full_name=full_name,
                        roll_number=roll_number,
                        department=department,
                        semester=int(semester)
                    )

                messages.success(
                    request,
                    'Account created successfully. Please log in.'
                )
                return redirect('login')

            except IntegrityError:
                messages.error(
                    request,
                    'Username, email or roll number is already registered.'
                )

    return render(request, 'signup.html')


def login(request):

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')
        return redirect('item_list')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            auth_login(request, user)

            if user.is_staff:
                return redirect('dashboard')

            return redirect('item_list')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout(request):

    if request.method == 'POST':
        auth_logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('landing')

    return redirect('landing')
