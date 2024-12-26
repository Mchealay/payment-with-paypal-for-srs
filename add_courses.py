import os
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'srs.settings')
django.setup()

from students.models import Course

# Create some sample courses
courses = [
    {"name": "Mathematics", "description": "Introduction to Mathematics"},
    {"name": "Science", "description": "Basics of Science"},
    {"name": "History", "description": "World History Overview"},
    {"name": "English", "description": "English Literature"},
    {"name": "Art", "description": "Fundamentals of Art"},
]

# Add courses to the database
for course in courses:
    Course.objects.get_or_create(name=course["name"], description=course["description"])

print("Courses added!")