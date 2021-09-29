from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course
from .forms import RegisterForm, CustomUserChangeForm

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = RegisterForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')
        })
    )
    search_fields = ('email',)
    ordering = ('email',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_number', 'name', 'credits')
    
