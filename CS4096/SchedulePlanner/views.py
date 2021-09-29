from django.shortcuts import render
from django.views import View, generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from SchedulePlanner.forms import RegisterForm
from .models import Course
class Index(View):
    template_name = "SchedulePlanner/index.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class Credits(View):
    template_name = "SchedulePlanner/credits.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class CourseList(generic.ListView):
    model = Course
    template_name = "SchedulePlanner/course_list.html"

class Register(CreateView):
    template_name = "registration/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy('login')
    success_message = "Your acount was created successfully!"

