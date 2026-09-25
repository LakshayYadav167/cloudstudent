import pytest
from accounts.models import User
from students.models import StudentProfile

@pytest.fixture
def custom_admin_user():
    user = User.objects.create_user(username='admin_test_cf', password='test-only-password', role='ADMIN')
    return user

@pytest.fixture
def teacher_user():
    return User.objects.create_user(username='teacher_test_cf', password='test-only-password', role='TEACHER')

@pytest.fixture
def student_user():
    return User.objects.create_user(username='student_test_cf', password='test-only-password', role='STUDENT')

@pytest.fixture
def student_profile(student_user):
    return StudentProfile.objects.create(user=student_user, enrollment_number='TEST001_cf', enrollment_date='2024-01-01', department='CS')
