from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q
from .models import AcademicRecord
from .forms import AcademicRecordForm
from accounts.mixins import AdminRequiredMixin, TeacherRequiredMixin, StudentRequiredMixin
from django.core.exceptions import PermissionDenied

class AcademicRecordListView(StudentRequiredMixin, ListView):
    model = AcademicRecord
    template_name = 'academics/record_list.html'
    context_object_name = 'records'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        # Isolation: Students see only their own records
        if user.role == 'STUDENT':
            qs = qs.filter(enrollment__student__user=user)
        # Teachers see records for their courses
        elif user.role == 'TEACHER':
            qs = qs.filter(enrollment__course__instructor=user)

        query = self.request.GET.get('q')
        course = self.request.GET.get('course')
        if query:
            qs = qs.filter(enrollment__student__user__username__icontains=query)
        if course:
            qs = qs.filter(enrollment__course__code__icontains=course)
            
        return qs.select_related('enrollment__student__user', 'enrollment__course')

class AcademicRecordDetailView(StudentRequiredMixin, DetailView):
    model = AcademicRecord
    template_name = 'academics/record_detail.html'
    context_object_name = 'record'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if user.role == 'STUDENT' and user != obj.enrollment.student.user:
            raise PermissionDenied("You can only view your own academic records.")
        if user.role == 'TEACHER' and obj.enrollment.course.instructor != user and user.role != 'ADMIN':
            raise PermissionDenied("You can only view records for courses you teach.")
        return obj

class AcademicRecordCreateView(TeacherRequiredMixin, CreateView):
    model = AcademicRecord
    form_class = AcademicRecordForm
    template_name = 'academics/record_form.html'
    success_url = reverse_lazy('academics:list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Limit enrollments dropdown for teachers
        if self.request.user.role == 'TEACHER':
            form.fields['enrollment'].queryset = form.fields['enrollment'].queryset.filter(course__instructor=self.request.user)
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Academic record created successfully.')
        return super().form_valid(form)

class AcademicRecordUpdateView(TeacherRequiredMixin, UpdateView):
    model = AcademicRecord
    form_class = AcademicRecordForm
    template_name = 'academics/record_form.html'
    
    def get_success_url(self):
        return reverse_lazy('academics:detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'TEACHER':
            return qs.filter(enrollment__course__instructor=self.request.user)
        return qs

    def form_valid(self, form):
        messages.success(self.request, 'Academic record updated successfully.')
        return super().form_valid(form)

class AcademicRecordDeleteView(AdminRequiredMixin, DeleteView):
    model = AcademicRecord
    template_name = 'academics/record_confirm_delete.html'
    success_url = reverse_lazy('academics:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Academic record deleted successfully.')
        return super().delete(request, *args, **kwargs)
