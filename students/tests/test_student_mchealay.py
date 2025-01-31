import pytest
from django.urls import reverse
from django.test import Client
from students.models import Student

@pytest.mark.django_db
def test_register_user_valid():
    client = Client()
    url = reverse('register_student')
    response = client.post(url, {'name': 'John Doe', 'email': 'john.doe@example.com', 'password': 'test123'})
    
    assert response.status_code == 302  # Check if the registration redirects successfully
    assert Student.objects.filter(email='john.doe@example.com').exists()

@pytest.mark.django_db
def test_register_user_duplicate_email():
    client = Client()
    # Create a student with the same email
    Student.objects.create(name='test', email='test@example.com', password='test')
    
    url = reverse('register_student')
    response = client.post(url, {'name': 'test', 'email': 'test@example.com', 'password': 'test'})
    
    assert response.status_code == 200  # Check that registration fails
    assert 'This email is already registered' in response.content.decode()

@pytest.mark.django_db
def test_register_user_invalid_email_format():
    client = Client()
    url = reverse('register_student')
    response = client.post(url, {'name': 'John Doe', 'email': 'invalidemail', 'password': 'test123'})
    
    assert response.status_code == 200  # Check that registration fails
    assert 'Enter a valid email address' in response.content.decode()

@pytest.mark.django_db
def test_register_user_incomplete_format():
    client = Client()
    url = reverse('register_student')
    
    # Test registering without password
    response = client.post(url, {'name': 'John Doe', 'email': 'john.doe@example.com'})
    assert response.status_code == 200
    assert 'This field is required' in response.content.decode()
    
    # Test registering without email
    response = client.post(url, {'name': 'John Doe', 'password': 'test123'})
    assert response.status_code == 200
    assert 'This field is required' in response.content.decode()
    
    # Test registering without name
    response = client.post(url, {'email': 'john.doe@example.com', 'password': 'test123'})
    assert response.status_code == 200
    assert 'This field is required' in response.content.decode()
    

    