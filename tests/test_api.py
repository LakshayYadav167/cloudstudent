import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from students.models import StudentProfile
from courses.models import Course, Enrollment
from academics.models import AcademicRecord

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_unauthenticated_access(api_client):
    url = reverse('student-list')
    resp = api_client.get(url)
    assert resp.status_code == 401

@pytest.mark.django_db
def test_admin_full_access(api_client, custom_admin_user, student_profile):
    api_client.force_authenticate(user=custom_admin_user)
    # Admin can list students
    url = reverse('student-list')
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert len(resp.data['results']) > 0

@pytest.mark.django_db
def test_student_isolation(api_client, student_user, student_profile):
    other_student = User.objects.create_user(username='other_s', role='STUDENT')
    other_profile = StudentProfile.objects.create(user=other_student, enrollment_number='TEST002', enrollment_date='2024-01-01')
    
    api_client.force_authenticate(user=student_user)
    url = reverse('student-list')
    resp = api_client.get(url)
    
    # Should only see their own profile
    assert resp.status_code == 200
    assert resp.data['results'][0]['enrollment_number'] == 'TEST001_cf'

    # Cannot update own profile (Read-only)
    url_detail = reverse('student-detail', kwargs={'pk': student_profile.pk})
    resp_put = api_client.put(url_detail, {'department': 'CS'})
    assert resp_put.status_code == 403

@pytest.mark.django_db
def test_teacher_course_isolation(api_client, teacher_user):
    api_client.force_authenticate(user=teacher_user)
    course = Course.objects.create(code='CS101', name='Intro', credits=3, semester=1, department='CS', instructor=teacher_user)
    other_course = Course.objects.create(code='CS102', name='Advanced', credits=3, semester=2, department='CS')
    
    url = reverse('course-list')
    resp = api_client.get(url)
    # Teachers can see all courses
    assert resp.status_code == 200
    assert len(resp.data['results']) >= 2

@pytest.mark.django_db
def test_duplicate_enrollment_api(api_client, custom_admin_user, student_profile):
    api_client.force_authenticate(user=custom_admin_user)
    course = Course.objects.create(code='CS101', name='Intro', credits=3, semester=1, department='CS')
    
    url = reverse('enrollment-list')
    data = {
        'student': student_profile.pk,
        'course': course.pk,
        'academic_year': '2023-2024',
        'semester': 1,
        'status': 'ENROLLED'
    }
    resp1 = api_client.post(url, data)
    assert resp1.status_code == 201
    
    # Duplicate
    resp2 = api_client.post(url, data)
    assert resp2.status_code == 400
    assert "already enrolled" in str(resp2.data) or "non_field_errors" in resp2.data

@pytest.mark.django_db
def test_academic_record_validation(api_client, custom_admin_user, student_profile):
    api_client.force_authenticate(user=custom_admin_user)
    course = Course.objects.create(code='CS101', name='Intro', credits=3, semester=1, department='CS')
    enrollment = Enrollment.objects.create(student=student_profile, course=course, academic_year='2023-2024', semester=1)
    
    url = reverse('academic-record-list')
    # Invalid marks
    resp = api_client.post(url, {
        'enrollment': enrollment.pk,
        'marks': 150,
        'attendance': 80
    })
    assert resp.status_code == 400
    assert 'marks' in resp.data

    # Valid data
    resp2 = api_client.post(url, {
        'enrollment': enrollment.pk,
        'marks': 85,
        'attendance': 90
    })
    assert resp2.status_code == 201
    # Grade should be auto-calculated (85 -> A)
    assert resp2.data['grade'] == 'A'

@pytest.mark.django_db
def test_dashboard_api(api_client, custom_admin_user):
    api_client.force_authenticate(user=custom_admin_user)
    url = reverse('dashboard-api')
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert 'total_students' in resp.data

@pytest.mark.django_db
def test_token_authentication(api_client, custom_admin_user):
    url = reverse('api-token-auth')
    # Generate token
    resp = api_client.post(url, {'username': 'admin_test_cf', 'password': 'test-only-password'})
    assert resp.status_code == 200
    assert 'token' in resp.data
    token = resp.data['token']
    
    # Use token
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token)
    resp2 = api_client.get(reverse('student-list'))
    assert resp2.status_code == 200

@pytest.mark.django_db
def test_pagination_and_filtering(api_client, custom_admin_user):
    api_client.force_authenticate(user=custom_admin_user)
    # Create courses
    for i in range(15):
        Course.objects.create(code=f'CS{i}', name=f'Course {i}', credits=3, semester=1, department='CS')
    
    url = reverse('course-list')
    resp = api_client.get(url)
    assert resp.status_code == 200
    assert 'count' in resp.data
    assert len(resp.data['results']) == 10  # Paginated to 10
    
    # Filter
    resp2 = api_client.get(url + '?department=CS')
    assert resp2.status_code == 200
    assert resp2.data['count'] >= 15
    
    # Search
    resp3 = api_client.get(url + '?search=CS1')
    assert resp3.status_code == 200
    assert len(resp3.data['results']) >= 1
