import pytest
from students.models import Student
from payments.models import Payment

@pytest.mark.django_db
def test_payment_creation():
    # Create a student
    student = Student.objects.create(name="Alice", email="alice@example.com", password="password123")

    # Create a payment for the student
    payment = Payment.objects.create(student=student, amount=100.00, status="Pending")

    # Verify the payment was created
    assert payment.id is not None
    assert payment.student == student
    assert payment.amount == 100.00
    assert payment.status == "Pending"

@pytest.mark.django_db
def test_payment_status_update():
    # Create a student and a payment
    student = Student.objects.create(name="Bob", email="bob@example.com", password="password123")
    payment = Payment.objects.create(student=student, amount=200.00, status="Pending")

    # Update the payment status
    payment.status = "Completed"
    payment.save()

    # Verify the status update
    updated_payment = Payment.objects.get(id=payment.id)
    assert updated_payment.status == "Completed"