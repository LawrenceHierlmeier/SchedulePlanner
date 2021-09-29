from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('credits/', views.Credits.as_view(), name='credits'),
    path('accounts/register/', views.Register.as_view(), name='register'),
    path('course_list/', views.CourseList.as_view(), name='course_list')
]