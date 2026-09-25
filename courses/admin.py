from django.contrib import admin
from .models import Course, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'credits', 'department', 'semester', 'instructor')
    list_filter = ('department', 'semester')
    search_fields = ('code', 'name')
    ordering = ('code',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'academic_year', 'semester', 'status')
    list_filter = ('academic_year', 'semester', 'status')
    search_fields = ('student__enrollment_number', 'course__code')
    ordering = ('-enrollment_date',)
