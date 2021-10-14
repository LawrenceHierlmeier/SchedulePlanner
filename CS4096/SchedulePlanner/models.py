from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class Course(models.Model):
    course_number = models.TextField()
    name = models.TextField()
    description = models.TextField()
    requirements = models.TextField()
    credits = models.IntegerField()
    full_text = models.TextField()

    def __str__(self):
        return f"{self.course_number} - {self.name}"

class User(AbstractUser):
    username = None
    email = models.EmailField("Email Address", unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    #m2m relationship with courses to list earned credits
    earned_credits = models.ManyToManyField(Course)

    #another m2m for planned courses, goes through "scheduled" class to keep track of planned semester
    planned_credits = models.ManyToManyField(Course, through="Scheduled")

    def __str__(self):
        return self.email
        
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

class Scheduled(models.Model):
    course = ForeignKey(Course, on_delete=models.CASCADE)
    user = ForeignKey(User, on_delete=models.CASCADE)
    #storing planned semester as text field for now - possibly stored as integer field, but we'd have to define a "semester 0"
    semester = models.TextField()