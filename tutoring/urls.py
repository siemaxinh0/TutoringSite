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
    path('student/', views.student_dashboard, name='student_dashboard'),
]
