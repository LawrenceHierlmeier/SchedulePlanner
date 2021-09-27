from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('credits/', views.Credits.as_view(), name='credits'),
    path('accounts/register/', views.Register.as_view(), name='register')
]