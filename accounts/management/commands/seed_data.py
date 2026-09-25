import random
from django.core.management.base import BaseCommand
from accounts.models import User
from students.models import StudentProfile
from courses.models import Course, Enrollment
from academics.models import AcademicRecord
from django.utils import timezone

class Command(BaseCommand):
    help = 'Seeds the database with fictional demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database seed...")

        # 1 Admin
        admin, _ = User.objects.get_or_create(username='admin', defaults={'role': 'ADMIN', 'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True})
        admin.set_password('Admin@123')
        admin.save()

        # 2 Teachers
        t1, _ = User.objects.get_or_create(username='teacher1', defaults={'role': 'TEACHER', 'first_name': 'Alice', 'last_name': 'Smith'})
        t1.set_password('Teacher@123')
        t1.save()
        t2, _ = User.objects.get_or_create(username='teacher2', defaults={'role': 'TEACHER', 'first_name': 'Bob', 'last_name': 'Jones'})
        t2.set_password('Teacher@123')
        t2.save()

        # 15 Students
        students = []
        for i in range(1, 16):
            u, _ = User.objects.get_or_create(username=f'student{i}', defaults={'role': 'STUDENT', 'first_name': f'Student{i}', 'last_name': 'Test'})
            u.set_password('Student@123')
            u.save()
            
            sp, _ = StudentProfile.objects.get_or_create(
                user=u,
                defaults={
                    'enrollment_number': f'ENR2024{i:03d}',
                    'date_of_birth': '2000-01-01',
                    'department': 'Computer Science',
                    'program': 'B.Tech',
                    'semester': 1,
                    'enrollment_date': timezone.now().date(),
                    'status': 'ACTIVE'
                }
            )
            students.append(sp)

        # 5 Courses
        courses = []
        for i, code in enumerate(['CS101', 'CS102', 'CS103', 'CS104', 'CS105']):
            c, _ = Course.objects.get_or_create(
                code=code,
                defaults={
                    'name': f'Course {code}',
                    'description': 'Demo course',
                    'credits': random.randint(3, 4),
                    'department': 'Computer Science',
                    'semester': 1,
                    'instructor': t1 if i % 2 == 0 else t2
                }
            )
            courses.append(c)

        # Enrollments & Academic Records
        for student in students:
            for course in random.sample(courses, 3):
                enrollment, created = Enrollment.objects.get_or_create(
                    student=student,
                    course=course,
                    academic_year='2023-2024',
                    semester=1,
                    defaults={'status': 'ENROLLED'}
                )
                if created:
                    marks = random.uniform(40.0, 98.0)
                    attendance = random.uniform(60.0, 100.0)
                    AcademicRecord.objects.get_or_create(
                        enrollment=enrollment,
                        defaults={'marks': marks, 'attendance': attendance}
                    )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
        self.stdout.write("Credentials:")
        self.stdout.write("Admin: admin / Admin@123")
        self.stdout.write("Teacher: teacher1 / Teacher@123")
        self.stdout.write("Student: student1 / Student@123")
