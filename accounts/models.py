
from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):

    DEPARTMENT_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Software Engineering', 'Software Engineering'),
        ('Information Technology', 'Information Technology'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Business Administration', 'Business Administration'),
        ('Other', 'Other'),
    ]

    SEMESTER_CHOICES = [
        (1, '1st Semester'),
        (2, '2nd Semester'),
        (3, '3rd Semester'),
        (4, '4th Semester'),
        (5, '5th Semester'),
        (6, '6th Semester'),
        (7, '7th Semester'),
        (8, '8th Semester'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    full_name = models.CharField(
        max_length=100
    )

    roll_number = models.CharField(
        max_length=30,
        unique=True
    )

    department = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES
    )

    semester = models.PositiveSmallIntegerField(
        choices=SEMESTER_CHOICES
    )

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"
