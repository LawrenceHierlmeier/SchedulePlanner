from django.shortcuts import render
from django.views import View, generic
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from SchedulePlanner.forms import RegisterForm
from .models import *
from .forms import CourseLogForm


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
    success_message = "Your account was created successfully!"


class CatalogDirectory(generic.ListView):
    model = Department
    template_name = "SchedulePlanner/catalog.html"

class DeptCourseList(generic.DetailView):
    model = Department
    form = CourseLogForm
    template_name = "SchedulePlanner/dept_course_list.html"
    slug_url_kwarg = "dept_slug"


class ListCourseLog(generic.ListView):
    model = User
    template_name = "SchedulePlanner/list_courselog.html"


def add_courselog(request):
    if request.method == "POST":
        form = CourseLogForm(request.POST)
        if form.is_valid():
            form.save()
            #return

    form = CourseLogForm()
    return render(request, "SchedulePlanner/add_courselog.html", {'form': form})




