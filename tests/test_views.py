import pytest
from django.urls import reverse
from accounts.models import User
from students.models import StudentProfile
from courses.models import Course, Enrollment
from academics.models import AcademicRecord

pytestmark = pytest.mark.django_db



def test_login_logout(client, custom_admin_user):
    # Login
    resp = client.post(reverse('accounts:login'), {'username': 'admin_test_cf', 'password': 'password123'})
    assert resp.status_code == 302
    
    # Logout
    resp = client.post(reverse('accounts:logout'))
    assert resp.status_code == 302

def test_role_authorization(client, student_user, student_profile):
    client.force_login(student_user)
    # Student cannot access add course (Admin only)
    resp = client.get(reverse('courses:add'))
    assert resp.status_code == 403
    
def test_student_crud_access(client, custom_admin_user, teacher_user):
    client.force_login(custom_admin_user)
    resp = client.get(reverse('students:add'))
    assert resp.status_code == 200
    
    client.force_login(teacher_user)
    resp = client.get(reverse('students:add'))
    assert resp.status_code == 403

def test_student_isolation(client, student_user, student_profile):
    other_student = User.objects.create_user(username='other', role='STUDENT')
    other_profile = StudentProfile.objects.create(user=other_student, enrollment_number='TEST002', enrollment_date='2024-01-01')
    
    client.force_login(student_user)
    # Can access own profile
    resp = client.get(reverse('students:detail', kwargs={'pk': student_profile.pk}))
    assert resp.status_code == 200
    
    # Cannot access other profile
    resp = client.get(reverse('students:detail', kwargs={'pk': other_profile.pk}))
    assert resp.status_code == 403

def test_duplicate_enrollment(client, custom_admin_user, student_profile):
    client.force_login(custom_admin_user)
    course = Course.objects.create(code='CS101', name='Intro', credits=3, semester=1, department='CS')
    
    # Create first enrollment
    resp1 = client.post(reverse('courses:enrollment_add'), {
        'student': student_profile.pk,
        'course': course.pk,
        'academic_year': '2023-2024',
        'semester': 1,
        'status': 'ENROLLED'
    })
    assert resp1.status_code == 302
    assert Enrollment.objects.count() == 1
    
    # Duplicate enrollment should fail validation and return 200 (form with errors)
    resp2 = client.post(reverse('courses:enrollment_add'), {
        'student': student_profile.pk,
        'course': course.pk,
        'academic_year': '2023-2024',
        'semester': 1,
        'status': 'ENROLLED'
    })
    assert resp2.status_code == 200
    assert 'This student is already enrolled' in str(resp2.content)
    assert Enrollment.objects.count() == 1

def test_course_crud(client, custom_admin_user, teacher_user):
    client.force_login(custom_admin_user)
    resp = client.get(reverse('courses:list'))
    assert resp.status_code == 200
    
    resp = client.post(reverse('courses:add'), {
        'code': 'CS201', 'name': 'Data Structures', 'description': 'Intro to Data Structures', 'credits': 4, 'semester': 2, 'department': 'CS', 'instructor': teacher_user.pk
    })
    if resp.status_code == 200:
        print(resp.context['form'].errors)
    assert resp.status_code == 302
    assert Course.objects.filter(code='CS201').exists()

def test_enrollment_crud(client, custom_admin_user, student_profile):
    client.force_login(custom_admin_user)
    course = Course.objects.create(code='CS101', name='Intro', credits=3, semester=1, department='CS')
    resp = client.get(reverse('courses:enrollment_list'))
    assert resp.status_code == 200

def test_academic_record_crud(client, custom_admin_user, student_profile):
    client.force_login(custom_admin_user)
    course = Course.objects.create(code='CS101', name='Intro', credits=3, semester=1, department='CS')
    enrollment = Enrollment.objects.create(student=student_profile, course=course, academic_year='2023-2024', semester=1, status='ENROLLED')
    resp = client.get(reverse('academics:list'))
    assert resp.status_code == 200
    
def test_academic_record_grade_calculation(client, custom_admin_user, student_profile):
    client.force_login(custom_admin_user)
    course = Course.objects.create(code='CS101', name='Intro', credits=3, semester=1, department='CS')
    enrollment = Enrollment.objects.create(student=student_profile, course=course, academic_year='2023-2024', semester=1, status='ENROLLED')
    resp = client.post(reverse('academics:add'), {
        'enrollment': enrollment.pk, 'marks': 95, 'attendance': 90
    })
    assert resp.status_code == 302
    record = AcademicRecord.objects.get(enrollment=enrollment)
    assert record.grade == 'A+'

def test_academic_record_isolation(client, student_user, student_profile):
    client.force_login(student_user)
    course = Course.objects.create(code='CS101', name='Intro', credits=3, semester=1, department='CS')
    enrollment = Enrollment.objects.create(student=student_profile, course=course, academic_year='2023-2024', semester=1, status='ENROLLED')
    record = AcademicRecord.objects.create(enrollment=enrollment, marks=80, attendance=80)
    
    other_student = User.objects.create_user(username='other3', role='STUDENT')
    other_profile = StudentProfile.objects.create(user=other_student, enrollment_number='TEST003', enrollment_date='2024-01-01')
    other_enrollment = Enrollment.objects.create(student=other_profile, course=course, academic_year='2023-2024', semester=1, status='ENROLLED')
    other_record = AcademicRecord.objects.create(enrollment=other_enrollment, marks=70, attendance=70)
    
    resp = client.get(reverse('academics:detail', kwargs={'pk': record.pk}))
    assert resp.status_code == 200
    
    resp = client.get(reverse('academics:detail', kwargs={'pk': other_record.pk}))
    assert resp.status_code == 403

def test_dashboard_view(client, custom_admin_user):
    client.force_login(custom_admin_user)
    resp = client.get(reverse('dashboard:index'))
    assert resp.status_code == 200
