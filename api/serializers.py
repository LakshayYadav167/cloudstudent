from rest_framework import serializers
from students.models import StudentProfile
from courses.models import Course, Enrollment
from academics.models import AcademicRecord
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['role']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='TEACHER'),
        source='instructor',
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    student_detail = StudentProfileSerializer(source='student', read_only=True)
    course_detail = CourseSerializer(source='course', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = '__all__'

    def validate(self, data):
        student = data.get('student')
        course = data.get('course')
        academic_year = data.get('academic_year')
        semester = data.get('semester')
        
        if self.instance:
            student = data.get('student', self.instance.student)
            course = data.get('course', self.instance.course)
            academic_year = data.get('academic_year', self.instance.academic_year)
            semester = data.get('semester', self.instance.semester)

        # Check for duplicates
        qs = Enrollment.objects.filter(
            student=student, 
            course=course, 
            academic_year=academic_year, 
            semester=semester
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
            
        if qs.exists():
            raise serializers.ValidationError("This student is already enrolled in this course for the given academic year and semester.")
            
        return data

class AcademicRecordSerializer(serializers.ModelSerializer):
    enrollment_detail = EnrollmentSerializer(source='enrollment', read_only=True)

    class Meta:
        model = AcademicRecord
        fields = ['id', 'enrollment', 'marks', 'attendance', 'grade', 'created_at', 'updated_at', 'enrollment_detail']
        read_only_fields = ['grade', 'created_at', 'updated_at']

    def validate_marks(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Marks must be between 0 and 100.")
        return value

    def validate_attendance(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Attendance must be between 0 and 100.")
        return value
