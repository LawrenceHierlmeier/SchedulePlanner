from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('credits/', views.Credits.as_view(), name='credits'),
    path('accounts/register/', views.Register.as_view(), name='register'),
    path('course_list/', views.CourseList.as_view(), name='course_list'),
    path('catalog_directory/', views.CatalogDirectory.as_view(), name='catalog_directory'),
    path('catalog/<slug:dept_slug>', views.DeptCourseList.as_view(), name='catalog_dept_course_list'),
    path('add_courselog', views.add_courselog, name='add_courselog'),
    path('list_courselog', views.ListCourseLog.as_view(), name='list_courselog'),
    #path('catalogs/aero-eng/', views.AeroEng.as_view(), name='aero_eng'),
    #path('catalogs/comp-sci/', views.CompSci.as_view(), name='comp_sci'),
]