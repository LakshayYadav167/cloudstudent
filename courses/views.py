from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q
from .models import Course, Enrollment
from .forms import CourseForm, EnrollmentForm
from accounts.mixins import AdminRequiredMixin, TeacherRequiredMixin, StudentRequiredMixin
from django.core.exceptions import PermissionDenied

# ==================== COURSE VIEWS ====================
class CourseListView(StudentRequiredMixin, ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        department = self.request.GET.get('department')
        if query:
            qs = qs.filter(
                Q(code__icontains=query) | 
                Q(name__icontains=query) | 
                Q(instructor__username__icontains=query)
            )
        if department:
            qs = qs.filter(department__icontains=department)
        return qs.select_related('instructor')

class CourseDetailView(StudentRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollment_count'] = self.object.enrollments.count()
        if self.request.user.role in ['ADMIN', 'TEACHER']:
            context['enrolled_students'] = self.object.enrollments.select_related('student__user')
        return context

class CourseCreateView(AdminRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:list')

    def form_valid(self, form):
        messages.success(self.request, 'Course created successfully.')
        return super().form_valid(form)

class CourseUpdateView(AdminRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    
    def get_success_url(self):
        return reverse_lazy('courses:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully.')
        return super().form_valid(form)

class CourseDeleteView(AdminRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Course deleted successfully.')
        return super().delete(request, *args, **kwargs)

# ==================== ENROLLMENT VIEWS ====================
class EnrollmentListView(TeacherRequiredMixin, ListView):
    model = Enrollment
    template_name = 'courses/enrollment_list.html'
    context_object_name = 'enrollments'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        course = self.request.GET.get('course')
        status = self.request.GET.get('status')
        if query:
            qs = qs.filter(student__user__username__icontains=query)
        if course:
            qs = qs.filter(course__code__icontains=course)
        if status:
            qs = qs.filter(status=status)
        return qs.select_related('student__user', 'course')

class EnrollmentDetailView(StudentRequiredMixin, DetailView):
    model = Enrollment
    template_name = 'courses/enrollment_detail.html'
    context_object_name = 'enrollment'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.role == 'STUDENT' and self.request.user != obj.student.user:
            raise PermissionDenied("You can only view your own enrollments.")
        return obj

class EnrollmentCreateView(AdminRequiredMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'courses/enrollment_form.html'
    success_url = reverse_lazy('courses:enrollment_list')

    def form_valid(self, form):
        messages.success(self.request, 'Enrollment created successfully.')
        return super().form_valid(form)

class EnrollmentDeleteView(AdminRequiredMixin, DeleteView):
    model = Enrollment
    template_name = 'courses/enrollment_confirm_delete.html'
    success_url = reverse_lazy('courses:enrollment_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Enrollment deleted successfully.')
        return super().delete(request, *args, **kwargs)
