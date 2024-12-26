from django.shortcuts import render, redirect
from .models import Payment
from students.models import Student
import paypalrestsdk

# PayPal configuration
paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" for production
    "client_id": "AVve5BwAPwz12DwQp8Wpedm7LA1yCW7Yk_g_-hinUD10o7PyKOatTfsqID-535eqEvOejsXYeRORBhYh",
    "client_secret": "EPcvHBMiX5547klo7SmXPp4MnaBh1YNfMZHguvJhe2lxEWIFOjEpbq0bXMId6AQ5DpgpzYew4_-VKESe"
})

def make_payment(request, student_id):
    student = Student.objects.get(id=student_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/payments/payment_success/",
                "cancel_url": "http://localhost:8000/payments/payment_cancel/"
            },
            "transactions": [{
                "amount": {
                    "total": amount,
                    "currency": "USD"
                },
                "description": "Payment for course registration."
            }]
        })

        if payment.create():
            # Redirect the user to PayPal for approval
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)
        else:
            return redirect('student_list')
    return render(request, 'make_payment.html', {'student': student})

def payment_success(request):
    # Handle successful payment
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        student_id = request.session.get('student_id')
        student = Student.objects.get(id=student_id)
        Payment.objects.create(student=student, amount=payment.transactions[0].amount.total, status='success')
        return render(request, 'payment_success.html', {'student': student})
    else:
        return render(request, 'payment_cancel.html')

def payment_cancel(request):
    # Handle payment cancellation
    return render(request, 'payment_cancel.html')