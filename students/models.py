from django.db import models
from django.contrib.auth.hashers import make_password, check_password
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password=models.CharField(max_length=22)
    registered_courses = models.ManyToManyField('Course', blank=True)
    def save(self, *args, **kwargs):
        if not self.pk:  # If the object is being created
            self.password = make_password(self.password)  # Hash the password
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

   
    def __str__(self):
        return  self.name
    #f"name:{self.name}, email:{self.email} ,password:{self.password}"

class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name