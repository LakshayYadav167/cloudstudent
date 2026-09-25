from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('enrollment_number', 'user', 'department', 'program', 'semester', 'status')
    list_filter = ('status', 'department', 'program', 'semester')
    search_fields = ('enrollment_number', 'user__username', 'user__first_name', 'user__last_name')
    ordering = ('enrollment_number',)
