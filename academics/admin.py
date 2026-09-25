from django.contrib import admin
from .models import AcademicRecord

@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'marks', 'attendance', 'grade')
    list_filter = ('grade',)
    search_fields = ('enrollment__student__enrollment_number', 'enrollment__course__code')
    ordering = ('-created_at',)
    readonly_fields = ('grade',)
