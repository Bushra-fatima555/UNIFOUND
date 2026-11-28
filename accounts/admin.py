
from django.contrib import admin
from django.contrib.auth.models import User
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = (
        'full_name',
        'roll_number',
        'department',
        'semester',
        'user',
    )

    search_fields = (
        'full_name',
        'roll_number',
        'user__username',
        'user__email',
    )

    list_filter = (
        'department',
        'semester',
    )

    ordering = ('full_name',)


