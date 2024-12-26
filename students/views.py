
from .models import Student, Course
from .forms import StudentForm, CourseForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login  # Renamed to avoid conflict
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import user
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')  # Get name from POST data
        email = request.POST.get('email')  # Get email from POST data
        password = request.POST.get('password')  # Get password from POST data
        
        try:
            # Fetch the student by email and check the name
            student = Student.objects.get(email=email)
            if student.name == name and student.check_password(password):  # Check name and password
                request.session['student_id'] = student.id  # Store student ID in session
                messages.success(request, 'Logged in successfully.')  # Success message
                return redirect('index')  # Redirect to the student list page
            else:
                messages.error(request, 'Invalid name or password.')  # Error message for invalid credentials
        except Student.DoesNotExist:
            messages.error(request, 'No student found with this email.')  # Error message for non-existent email
    
    return render(request, 'login.html')
def register_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student registered successfully.')
            return redirect('success')
    else:
        form = StudentForm()
    return render(request, 'register_student.html', {'form': form})


@login_required
def student_list(request): 
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})
@login_required
def register_course(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        course_ids = request.POST.getlist('course_ids')  # Get list of selected course IDs
        for course_id in course_ids:
            course = get_object_or_404(Course, id=course_id)
            student.registered_courses.add(course)
            
        return redirect('student_list')
    
    # Get all courses to display
    courses = Course.objects.all()
    return render(request, 'register_course.html', {'student': student, 'courses': courses})

def success_view(request):
    return render(request, 'success.html')  # Render the success template

@login_required  # Ensure only authenticated users can access this view
def index(request):
    student = request.user  # Assuming the logged-in user is a Student
    return render(request, 'index.html', {'student': student})  # Pass the student to the template