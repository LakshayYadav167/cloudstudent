from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg
from .serializers import (
    StudentProfileSerializer, CourseSerializer,
    EnrollmentSerializer, AcademicRecordSerializer
)
from students.models import StudentProfile
from courses.models import Course, Enrollment
from academics.models import AcademicRecord
from .permissions import RoleBasedPermission, IsAdminOrReadOnly

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentProfileSerializer
    permission_classes = [RoleBasedPermission, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'program', 'semester', 'status']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'enrollment_number']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.role == 'TEACHER':
            return StudentProfile.objects.select_related('user').all()
        elif user.role == 'STUDENT':
            return StudentProfile.objects.filter(user=user).select_related('user')
        return StudentProfile.objects.none()

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [RoleBasedPermission, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'semester']
    search_fields = ['code', 'name', 'instructor__first_name', 'instructor__last_name']

    def get_queryset(self):
        # All roles can see all courses for listing
        return Course.objects.select_related('instructor').all()

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [RoleBasedPermission, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'course', 'academic_year', 'semester', 'status']

    def get_queryset(self):
        user = self.request.user
        qs = Enrollment.objects.select_related('student__user', 'course').all()
        
        if user.role == 'ADMIN':
            return qs
        elif user.role == 'TEACHER':
            # Teachers only see enrollments for courses they teach
            return qs.filter(course__instructor=user)
        elif user.role == 'STUDENT':
            try:
                sp = user.student_profile
                return qs.filter(student=sp)
            except StudentProfile.DoesNotExist:
                return Enrollment.objects.none()
        return Enrollment.objects.none()

class AcademicRecordViewSet(viewsets.ModelViewSet):
    serializer_class = AcademicRecordSerializer
    permission_classes = [RoleBasedPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['enrollment', 'enrollment__student', 'enrollment__course']

    def get_queryset(self):
        user = self.request.user
        qs = AcademicRecord.objects.select_related('enrollment__student__user', 'enrollment__course').all()
        
        if user.role == 'ADMIN':
            return qs
        elif user.role == 'TEACHER':
            # Teachers only see records for courses they teach
            return qs.filter(enrollment__course__instructor=user)
        elif user.role == 'STUDENT':
            try:
                sp = user.student_profile
                return qs.filter(enrollment__student=sp)
            except StudentProfile.DoesNotExist:
                return AcademicRecord.objects.none()
        return AcademicRecord.objects.none()

class DashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        role = user.role
        data = {}

        if role == 'ADMIN':
            data['total_students'] = StudentProfile.objects.count()
            data['total_courses'] = Course.objects.count()
            data['total_enrollments'] = Enrollment.objects.count()
            data['avg_marks'] = AcademicRecord.objects.aggregate(Avg('marks'))['marks__avg'] or 0
            data['avg_attendance'] = AcademicRecord.objects.aggregate(Avg('attendance'))['attendance__avg'] or 0
            
            data['recent_students'] = StudentProfileSerializer(
                StudentProfile.objects.order_by('-created_at')[:5], many=True).data
            data['recent_enrollments'] = EnrollmentSerializer(
                Enrollment.objects.select_related('student__user', 'course').order_by('-enrollment_date')[:5], many=True).data
            data['recent_records'] = AcademicRecordSerializer(
                AcademicRecord.objects.select_related('enrollment__student__user', 'enrollment__course').order_by('-created_at')[:5], many=True).data
                
        elif role == 'TEACHER':
            my_courses = Course.objects.filter(instructor=user)
            data['courses_taught'] = my_courses.count()
            data['total_students'] = Enrollment.objects.filter(course__in=my_courses).values('student').distinct().count()
            data['recent_records'] = AcademicRecordSerializer(
                AcademicRecord.objects.filter(enrollment__course__in=my_courses).select_related('enrollment__student__user', 'enrollment__course').order_by('-created_at')[:5], many=True).data
            
        elif role == 'STUDENT':
            try:
                sp = user.student_profile
                data['student_profile'] = StudentProfileSerializer(sp).data
                data['enrolled_courses'] = Enrollment.objects.filter(student=sp).count()
                my_records = AcademicRecord.objects.filter(enrollment__student=sp)
                data['avg_marks'] = my_records.aggregate(Avg('marks'))['marks__avg'] or 0
                data['avg_attendance'] = my_records.aggregate(Avg('attendance'))['attendance__avg'] or 0
                data['recent_records'] = AcademicRecordSerializer(
                    my_records.select_related('enrollment__course').order_by('-created_at')[:5], many=True).data
            except StudentProfile.DoesNotExist:
                pass
                
        return Response(data)
