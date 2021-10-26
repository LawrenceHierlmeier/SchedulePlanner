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

    #m2m relationship with courses to list planned/taken courses
    planned_credits = models.ManyToManyField(Course, through="CreditHour")

    def __str__(self):
        return self.email
        
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

#class for keeping track of taken and/or planned credits, dependent on scheduled date
class CreditHour(models.Model):
    course = ForeignKey(Course, on_delete=models.CASCADE)
    user = ForeignKey(User, on_delete=models.CASCADE)
    #storing date of course start - ashton's semester calculation is now used for semester
    date = models.TextField()

    @property
    def semester(self):
        if self.date.month == 1:
            season = "Spring"
        elif self.date.month == 6:
            season = "Summer"
        elif self.date.month == 8:
            season = "Fall"
        else:
            raise RuntimeError(f"{self.date.month} is an invalid")
        return f"{season} {self.date.year}"