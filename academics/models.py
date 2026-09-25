from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from courses.models import Enrollment

class AcademicRecord(models.Model):
    # The OneToOneField enforces that only one AcademicRecord can exist per Enrollment.
    # Enrollment already enforces the unique constraint on (student, course, academic_year, semester).
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='academic_record')
    
    marks = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    attendance = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    grade = models.CharField(max_length=2, blank=True, help_text="Calculated automatically based on marks")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Business logic for grade calculation
        if self.marks >= 90:
            self.grade = 'A+'
        elif self.marks >= 80:
            self.grade = 'A'
        elif self.marks >= 70:
            self.grade = 'B'
        elif self.marks >= 60:
            self.grade = 'C'
        elif self.marks >= 50:
            self.grade = 'D'
        else:
            self.grade = 'F'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.enrollment.student.enrollment_number} - {self.enrollment.course.code} - {self.grade}"
