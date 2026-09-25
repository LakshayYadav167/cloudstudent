from django import forms
from .models import Course, Enrollment

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'credits', 'department', 'semester', 'instructor']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'academic_year', 'semester', 'status']

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        course = cleaned_data.get('course')
        academic_year = cleaned_data.get('academic_year')
        semester = cleaned_data.get('semester')

        if student and course and academic_year and semester:
            if Enrollment.objects.filter(
                student=student, 
                course=course, 
                academic_year=academic_year, 
                semester=semester
            ).exclude(pk=self.instance.pk if self.instance else None).exists():
                raise forms.ValidationError("This student is already enrolled in this course for this term.")
        return cleaned_data
