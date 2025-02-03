import pytest
from students.models import Student, Course

@pytest.mark.django_db
def test_student_creation():
    # Create a student
    student = Student.objects.create(name="John Doe", email="john@example.com", password="password123")

    # Verify the student was created
    assert student.id is not None
    assert student.name == "John Doe"
    assert student.email == "john@example.com"

    # Verify the password is hashed
    assert student.password != "password123"  # Password should be hashed
    assert student.check_password("password123")  # Verify password check works

@pytest.mark.django_db
def test_student_course_registration():
    # Create a student and a course
    student = Student.objects.create(name="Jane Doe", email="jane@example.com", password="password123")
    course = Course.objects.create(name="Mathematics", description="Advanced Algebra")

    # Register the student for the course
    student.registered_courses.add(course)

    # Verify the course registration
    assert student.registered_courses.count() == 1
    assert student.registered_courses.first().name == "Mathematics"