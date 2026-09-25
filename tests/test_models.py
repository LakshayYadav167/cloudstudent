import pytest
from django.db import IntegrityError
from accounts.models import User
from students.models import StudentProfile
from courses.models import Course, Enrollment
from academics.models import AcademicRecord
from django.utils import timezone

@pytest.mark.django_db
class TestModels:
    def test_user_roles(self):
        admin = User.objects.create_user(username='admin_test', role='ADMIN')
        student = User.objects.create_user(username='student_test', role='STUDENT')
        teacher = User.objects.create_user(username='teacher_test', role='TEACHER')
        assert admin.role == 'ADMIN'
        assert student.role == 'STUDENT'
        assert teacher.role == 'TEACHER'

    def test_unique_enrollment_number(self):
        u1 = User.objects.create_user(username='s1', role='STUDENT')
        u2 = User.objects.create_user(username='s2', role='STUDENT')
        
        StudentProfile.objects.create(user=u1, enrollment_number='E001', enrollment_date=timezone.now().date())
        with pytest.raises(IntegrityError):
            StudentProfile.objects.create(user=u2, enrollment_number='E001', enrollment_date=timezone.now().date())

    def test_unique_course_code(self):
        Course.objects.create(code='CS101', credits=3, semester=1)
        with pytest.raises(IntegrityError):
            Course.objects.create(code='CS101', credits=4, semester=2)

    def test_duplicate_enrollment_prevention(self):
        u1 = User.objects.create_user(username='s3', role='STUDENT')
        sp = StudentProfile.objects.create(user=u1, enrollment_number='E002', enrollment_date=timezone.now().date())
        c = Course.objects.create(code='CS102', credits=3, semester=1)

        Enrollment.objects.create(student=sp, course=c, academic_year='2023', semester=1)
        with pytest.raises(IntegrityError):
            Enrollment.objects.create(student=sp, course=c, academic_year='2023', semester=1)

    def test_academic_record_one_to_one(self):
        u1 = User.objects.create_user(username='s4', role='STUDENT')
        sp = StudentProfile.objects.create(user=u1, enrollment_number='E003', enrollment_date=timezone.now().date())
        c = Course.objects.create(code='CS103', credits=3, semester=1)
        e = Enrollment.objects.create(student=sp, course=c, academic_year='2023', semester=1)

        AcademicRecord.objects.create(enrollment=e, marks=95, attendance=80)
        with pytest.raises(IntegrityError):
            AcademicRecord.objects.create(enrollment=e, marks=90, attendance=70)

    def test_grade_calculation(self):
        u1 = User.objects.create_user(username='s5', role='STUDENT')
        sp = StudentProfile.objects.create(user=u1, enrollment_number='E004', enrollment_date=timezone.now().date())
        c = Course.objects.create(code='CS104', credits=3, semester=1)
        e = Enrollment.objects.create(student=sp, course=c, academic_year='2023', semester=1)

        ar = AcademicRecord.objects.create(enrollment=e, marks=85, attendance=80)
        assert ar.grade == 'A'

        ar.marks = 45
        ar.save()
        assert ar.grade == 'F'

        ar.marks = 92
        ar.save()
        assert ar.grade == 'A+'
