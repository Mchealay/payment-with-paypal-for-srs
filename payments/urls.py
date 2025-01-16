from django.urls import path
from .views import make_payment, payment_success, payment_cancel

urlpatterns = [
    path('payment/<int:student_id>/', make_payment, name='make_payment'),
    path('payment_success/', payment_success, name='payment_success'),
    path('payment_cancel/', payment_cancel, name='payment_cancel'),
]
