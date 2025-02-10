import pytest
from students.models import Student, Course
from django.contrib.auth.hashers import check_password

@pytest.mark.django_db
def test_student_creation():
    # Create a student
    student = Student.objects.create(
        name="John Doe",
        email="john@example.com",
        password="securepassword123"
    )

    # Check if the student was created
    assert student.name == "John Doe"
    assert student.email == "john@example.com"
    assert check_password("securepassword123", student.password)  # Verify password hashing

@pytest.mark.django_db
def test_student_course_registration():
    # Create a student and a course
    student = Student.objects.create(
        name="Jane Doe",
        email="jane@example.com",
        password="securepassword123"
    )
    course = Course.objects.create(
        name="Mathematics",
        description="Advanced Mathematics Course"
    )

    # Register the course for the student
    student.registered_courses.add(course)

    # Check if the course is registered for the student
    assert course in student.registered_courses.all()