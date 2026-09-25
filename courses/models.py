from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from students.models import StudentProfile

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    credits = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    department = models.CharField(max_length=100)
    semester = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='taught_courses', limit_choices_to={'role': 'TEACHER'})

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Enrollment(models.Model):
    class Status(models.TextChoices):
        ENROLLED = 'ENROLLED', 'Enrolled'
        COMPLETED = 'COMPLETED', 'Completed'
        DROPPED = 'DROPPED', 'Dropped'

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    academic_year = models.CharField(max_length=9, help_text="e.g., 2023-2024")
    semester = models.PositiveIntegerField()
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ENROLLED)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course', 'academic_year', 'semester'],
                name='unique_student_course_enrollment'
            )
        ]

    def __str__(self):
        return f"{self.student.enrollment_number} -> {self.course.code} ({self.academic_year} S{self.semester})"
