from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q
from .models import StudentProfile
from .forms import StudentProfileForm
from accounts.mixins import AdminRequiredMixin, TeacherRequiredMixin, StudentRequiredMixin
from django.core.exceptions import PermissionDenied

class StudentListView(TeacherRequiredMixin, ListView):
    model = StudentProfile
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')
        department = self.request.GET.get('department')
        if query:
            qs = qs.filter(
                Q(user__first_name__icontains=query) | 
                Q(user__last_name__icontains=query) | 
                Q(user__email__icontains=query) |
                Q(enrollment_number__icontains=query)
            )
        if department:
            qs = qs.filter(department__icontains=department)
        return qs.select_related('user')

class StudentDetailView(StudentRequiredMixin, DetailView):
    model = StudentProfile
    template_name = 'students/student_detail.html'
    context_object_name = 'student'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.role == 'STUDENT' and self.request.user != obj.user:
            raise PermissionDenied("You can only view your own profile.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = self.object.enrollments.select_related('course').all()
        return context

class StudentCreateView(AdminRequiredMixin, CreateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:list')

    def form_valid(self, form):
        messages.success(self.request, 'Student created successfully.')
        return super().form_valid(form)

class StudentUpdateView(AdminRequiredMixin, UpdateView):
    model = StudentProfile
    form_class = StudentProfileForm
    template_name = 'students/student_form.html'
    
    def get_success_url(self):
        return reverse_lazy('students:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Student updated successfully.')
        return super().form_valid(form)

class StudentDeleteView(AdminRequiredMixin, DeleteView):
    model = StudentProfile
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Student deleted successfully.')
        return super().delete(request, *args, **kwargs)
