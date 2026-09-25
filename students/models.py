from django.db import models
from accounts.models import User

class StudentProfile(models.Model):
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'
        OTHER = 'OTHER', 'Other'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        GRADUATED = 'GRADUATED', 'Graduated'
        SUSPENDED = 'SUSPENDED', 'Suspended'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', limit_choices_to={'role': 'STUDENT'})
    enrollment_number = models.CharField(max_length=50, unique=True, db_index=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True, null=True)
    department = models.CharField(max_length=100)
    program = models.CharField(max_length=100)
    semester = models.PositiveIntegerField(default=1)
    enrollment_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    address = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        full_name = self.user.get_full_name()
        display_name = full_name if full_name else self.user.username
        return f"{display_name} ({self.enrollment_number})"
