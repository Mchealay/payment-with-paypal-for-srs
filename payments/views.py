from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from students.models import Student
import paypalrestsdk
paypalrestsdk.configure({
    "mode": "sandbox", 
    "client_id": "Af6uWJiXWpLIBLriA-WLaprr_YOdlmeZQ8ZmIvilfXnEqCRwcAqQnDynqqS9oLlid2OTRVbs9CtZGfnl",
    "client_secret": "EOHCtmRSxCQrpSx90SyI3tCshxlOQLb4-8VhXwURwWv1Krc695-LWc-kvzVHPJ5UEHoKyaUheufgSGbm"
})
#sb-vzrnx35521597@business.example.com seller 12345678
#sb-gn67u35482760@personal.example.com buyer 12345678 
def make_payment(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": f"http://localhost:8000/payments/payment_success/?student_id={student.id}",
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
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)
        else:
            return redirect('student_list')
    return render(request, 'make_payment.html', {'student': student})

def payment_success(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')
    student_id = request.GET.get('student_id')

    payment = paypalrestsdk.Payment.find(payment_id)
    if payment.execute({"payer_id": payer_id}):
        student = get_object_or_404(Student, id=student_id)  # Get the student using the ID from the query
        Payment.objects.create(student=student, amount=payment.transactions[0].amount.total, status='success')
        return render(request, 'payment_success.html', {'student': student})
    else:
        return render(request, 'payment_cancel.html')

def payment_cancel(request):
    # Handle payment cancellation
    return render(request, 'payment_cancel.html')