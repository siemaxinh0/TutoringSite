from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='tutoring/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('redirect/', views.login_success_redirect, name='login_success_redirect'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/add-availability/', views.add_availability, name='add_availability'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/add-availability/', views.student_add_availability, name='student_add_availability'),
    path('availability/delete/<int:availability_id>/', views.delete_availability, name='delete_availability'),
]
