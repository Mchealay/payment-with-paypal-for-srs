import pytest
from django.urls import reverse
from django.test import Client
from students.models import Student, Course

@pytest.mark.django_db
def test_login_view_success():
    # Create a student
    student = Student.objects.create(
        name="John Doe",
        email="john@example.com",
        password="securepassword123"
    )

    # Simulate a POST request to the login view
    client = Client()
    response = client.post(reverse('login'), {  # Use 'login' instead of 'login_view'
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'securepassword123'
    })

    # Check if the login was successful
    assert response.status_code == 302  # Redirect status code
    assert response.url == reverse('index')  # Redirects to the index page

@pytest.mark.django_db
def test_login_view_failure():
    # Simulate a POST request with invalid credentials
    client = Client()
    response = client.post(reverse('login'), { 
        'name': 'Invalid Name',
        'email': 'invalid@example.com',
        'password': 'wrongpassword'
    })

    # Check if the login failed
    assert response.status_code == 200  # Stays on the login page
    assert b'Invalid name or password' in response.content  # Error message

@pytest.mark.django_db
def test_register_student_view():
    client = Client()
    response = client.post(reverse('register_student'), {  # Use 'register_student'
        'name': 'Alice',
        'email': 'alice@example.com',
        'password': 'alicepassword123'
    })

    # Check if the student was registered successfully
    assert response.status_code == 302  # Redirect status code
    assert response.url == reverse('success')  # Redirects to the success page

    # Verify the student was created in the database
    assert Student.objects.filter(email='alice@example.com').exists()

@pytest.mark.django_db
def test_student_list_view():
    # Create a student
    Student.objects.create(
        name="Bob",
        email="bob@example.com",
        password="bobpassword123"
    )

    # Simulate a GET request to the student list view
    client = Client()
    response = client.get(reverse('student_list'))  # Use 'student_list'

    # Check if the student list is displayed
    assert response.status_code == 200
    assert b'Bob' in response.content  # Student name appears in the response

@pytest.mark.django_db
def test_register_course_view():
    # Create a student and a course
    student = Student.objects.create(
        name="Charlie",
        email="charlie@example.com",
        password="charliepassword123"
    )
    course = Course.objects.create(
        name="Physics",
        description="Introduction to Physics"
    )

    # Simulate a POST request to register the course
    client = Client()
    response = client.post(reverse('register_course', args=[student.id]), {
        'course_ids': [course.id]
    })

    # Check if the course was registered successfully
    assert response.status_code == 302  # Redirect status code
    assert response.url == reverse('student_list')  # Redirects to the student list page

    # Verify the course is registered for the student
    assert course in student.registered_courses.all()