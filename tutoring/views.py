from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render

from .forms import AvailabilityForm, CustomUserCreationForm
from .models import Availability


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_success_redirect')
    else:
        form = CustomUserCreationForm()
    return render(request, 'tutoring/register.html', {'form': form})


@login_required
def login_success_redirect(request):
    user_roles = request.user.roles.values_list('role_name', flat=True)
    if 'Nauczyciel' in user_roles:
        return redirect('teacher_dashboard')
    if 'Uczeń' in user_roles:
        return redirect('student_dashboard')
    return redirect('dashboard')


@login_required
def dashboard(request):
    return render(request, 'tutoring/dashboard.html')


def is_teacher(user):
    return user.roles.filter(role_name='Nauczyciel').exists()


def is_student(user):
    return user.roles.filter(role_name='Uczeń').exists()


@login_required
@user_passes_test(is_teacher, login_url='dashboard')
def teacher_dashboard(request):
    availabilities = Availability.objects.filter(user=request.user)
    return render(request, 'tutoring/teacher_dashboard.html', {'availabilities': availabilities})


@login_required
@user_passes_test(is_teacher, login_url='dashboard')
def add_availability(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.user = request.user
            availability.save()
            return redirect('teacher_dashboard')
    else:
        form = AvailabilityForm()
    return render(request, 'tutoring/add_availability.html', {'form': form})


@login_required
@user_passes_test(is_student, login_url='dashboard')
def student_dashboard(request):
    return render(request, 'tutoring/student_dashboard.html')
