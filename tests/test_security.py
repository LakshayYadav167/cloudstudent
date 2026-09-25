import pytest
from django.urls import reverse
from courses.models import Course, Enrollment
from academics.models import AcademicRecord
from students.models import StudentProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_security_headers(client):
    resp = client.get(reverse('accounts:login'))
    assert resp.status_code == 200
    assert resp.headers.get('X-Frame-Options') == 'DENY'
    assert resp.headers.get('X-Content-Type-Options') == 'nosniff'
    assert resp.headers.get('Referrer-Policy') == 'same-origin'

@pytest.mark.django_db
def test_teacher_idor_academic_record_update(client, teacher_user, student_profile):
    # Teacher does not teach this course
    other_teacher = User.objects.create_user(username='other_t', role='TEACHER', password='password')
    course = Course.objects.create(code='CS999', name='Test Course', credits=3, semester=1, department='CS', instructor=other_teacher)
    enrollment = Enrollment.objects.create(student=student_profile, course=course, academic_year='2023-2024', semester=1, status='ENROLLED')
    record = AcademicRecord.objects.create(enrollment=enrollment, marks=90, attendance=90)
    
    # Login as our standard teacher (who does NOT teach CS999)
    client.force_login(teacher_user)
    
    # Attempt to access the update view
    resp = client.get(reverse('academics:edit', kwargs={'pk': record.pk}))
    # Expect 404 because get_queryset filters it out!
    assert resp.status_code == 404

@pytest.mark.django_db
def test_student_idor_enrollment_detail(client, student_user):
    # Another student's enrollment
    other_student = User.objects.create_user(username='other_s', role='STUDENT', password='password')
    other_profile = StudentProfile.objects.create(user=other_student, enrollment_number='TEST099', enrollment_date='2024-01-01')
    course = Course.objects.create(code='CS998', name='Test Course 2', credits=3, semester=1, department='CS')
    enrollment = Enrollment.objects.create(student=other_profile, course=course, academic_year='2023-2024', semester=1, status='ENROLLED')
    
    # Login as our standard student
    client.force_login(student_user)
    
    resp = client.get(reverse('courses:enrollment_detail', kwargs={'pk': enrollment.pk}))
    # Expect 403 Forbidden because of PermissionDenied in get_object
    assert resp.status_code == 403

@pytest.mark.django_db
def test_api_admin_only_write_course(api_client, teacher_user, custom_admin_user):
    course = Course.objects.create(code='CS997', name='Test Course 3', credits=3, semester=1, department='CS', instructor=teacher_user)
    url = reverse('course-detail', kwargs={'pk': course.pk})
    
    # Teacher attempting to DELETE course
    api_client.force_authenticate(user=teacher_user)
    resp = api_client.delete(url)
    assert resp.status_code == 403 # IsAdminOrReadOnly should block this!
    
    # Admin attempting to DELETE course
    api_client.force_authenticate(user=custom_admin_user)
    resp_admin = api_client.delete(url)
    assert resp_admin.status_code == 204
