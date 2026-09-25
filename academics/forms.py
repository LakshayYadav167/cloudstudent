from django import forms
from .models import AcademicRecord

class AcademicRecordForm(forms.ModelForm):
    class Meta:
        model = AcademicRecord
        fields = ['enrollment', 'marks', 'attendance']
        # Do not include 'grade' as it's auto-calculated by the backend!
