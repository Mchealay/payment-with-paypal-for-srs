from django.urls import path
from .views import register_student, student_list, register_course ,login_view,success_view,index

urlpatterns = [
     path('', login_view, name='login'),
    path('register/', register_student, name='register_student'),
    path('students/', student_list, name='student_list'),
    path('register_course/<int:student_id>/', register_course, name='register_course'),
     path('success/', success_view, name='success'),
     path('index/',index,name='index')
   ]