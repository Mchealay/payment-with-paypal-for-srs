import pytest
from students.models import Student
from payments.models import Payment

@pytest.mark.django_db
def test_student_payment_relationship():
    # Create a student
    student = Student.objects.create(name="Charlie", email="charlie@example.com", password="password123")

    # Create multiple payments for the student
    Payment.objects.create(student=student, amount=50.00, status="Pending")
    Payment.objects.create(student=student, amount=100.00, status="Completed")

    # Verify the payments are associated with the student
    assert student.payment_set.count() == 2
    assert student.payment_set.first().amount == 50.00
    assert student.payment_set.last().amount == 100.00

@pytest.mark.django_db
def test_student_with_multiple_payments():
    # Create a student
    student = Student.objects.create(name="Eve", email="eve@example.com", password="password123")

    # Create payments for the student
    Payment.objects.create(student=student, amount=75.00, status="Pending")
    Payment.objects.create(student=student, amount=150.00, status="Completed")

    # Verify the student and payments
    assert student.payment_set.count() == 2
    assert student.payment_set.first().amount == 75.00
    assert student.payment_set.last().amount == 150.00