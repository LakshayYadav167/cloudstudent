from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg
from students.models import StudentProfile
from courses.models import Course, Enrollment
from academics.models import AcademicRecord

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        role = user.role

        if role == 'ADMIN':
            context['total_students'] = StudentProfile.objects.count()
            context['total_courses'] = Course.objects.count()
            context['total_enrollments'] = Enrollment.objects.count()
            context['avg_marks'] = AcademicRecord.objects.aggregate(Avg('marks'))['marks__avg'] or 0
            context['avg_attendance'] = AcademicRecord.objects.aggregate(Avg('attendance'))['attendance__avg'] or 0
            
            context['recent_students'] = StudentProfile.objects.order_by('-created_at')[:5]
            context['recent_enrollments'] = Enrollment.objects.select_related('student__user', 'course').order_by('-enrollment_date')[:5]
            context['recent_records'] = AcademicRecord.objects.select_related('enrollment__student__user', 'enrollment__course').order_by('-created_at')[:5]
            
        elif role == 'TEACHER':
            my_courses = Course.objects.filter(instructor=user)
            context['courses_taught'] = my_courses.count()
            context['total_students'] = Enrollment.objects.filter(course__in=my_courses).values('student').distinct().count()
            
            context['my_courses_list'] = my_courses[:5]
            context['recent_records'] = AcademicRecord.objects.filter(enrollment__course__in=my_courses).select_related('enrollment__student__user', 'enrollment__course').order_by('-created_at')[:5]

        elif role == 'STUDENT':
            try:
                sp = user.student_profile
                context['student_profile'] = sp
                context['enrolled_courses'] = Enrollment.objects.filter(student=sp).count()
                my_records = AcademicRecord.objects.filter(enrollment__student=sp)
                context['avg_marks'] = my_records.aggregate(Avg('marks'))['marks__avg'] or 0
                context['avg_attendance'] = my_records.aggregate(Avg('attendance'))['attendance__avg'] or 0
                context['recent_records'] = my_records.select_related('enrollment__course').order_by('-created_at')[:5]
            except StudentProfile.DoesNotExist:
                context['student_profile'] = None

        return context
