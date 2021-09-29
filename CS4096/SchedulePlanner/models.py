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

class User(AbstractUser):
    username = None
    email = models.EmailField("Email Address", unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
        
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"