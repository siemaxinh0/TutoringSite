from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AvailabilityForm, CustomUserCreationForm, StudentRequirementForm
from .models import Availability, Role, StudentRequirement, User


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            student_role, _ = Role.objects.get_or_create(role_name='Uczeń')
            user.roles.add(student_role)
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
    availabilities = Availability.objects.filter(user=request.user)
    requirements = StudentRequirement.objects.filter(student=request.user)
    return render(request, 'tutoring/student_dashboard.html', {
        'availabilities': availabilities,
        'requirements': requirements,
    })


@login_required
@user_passes_test(is_student, login_url='dashboard')
def add_student_requirement(request):
    if request.method == 'POST':
        form = StudentRequirementForm(request.POST)
        if form.is_valid():
            requirement = form.save(commit=False)
            requirement.student = request.user
            requirement.save()
            return redirect('student_dashboard')
    else:
        form = StudentRequirementForm()
    return render(request, 'tutoring/add_student_requirement.html', {'form': form})


@login_required
@user_passes_test(is_student, login_url='dashboard')
def student_add_availability(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.user = request.user
            availability.save()
            return redirect('student_dashboard')
    else:
        form = AvailabilityForm()
    return render(request, 'tutoring/student_add_availability.html', {'form': form})


@login_required
def delete_availability(request, availability_id):
    availability = get_object_or_404(Availability, id=availability_id, user=request.user)
    availability.delete()
    user_roles = request.user.roles.values_list('role_name', flat=True)
    if 'Nauczyciel' in user_roles:
        return redirect('teacher_dashboard')
    if 'Uczeń' in user_roles:
        return redirect('student_dashboard')
    return redirect('dashboard')


@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='dashboard')
def admin_matching_panel(request):
    requirements = StudentRequirement.objects.select_related('student', 'subject').all()
    matching_results = []

    for req in requirements:
        student_avails = Availability.objects.filter(user=req.student)
        teachers = User.objects.filter(subjects=req.subject, roles__role_name='Nauczyciel').distinct()
        teacher_matches = []

        for teacher in teachers:
            teacher_avails = Availability.objects.filter(user=teacher)
            common_slots = 0
            for sa in student_avails:
                for ta in teacher_avails:
                    if sa.day_of_week == ta.day_of_week:
                        overlap_start = max(sa.start_time, ta.start_time)
                        overlap_end = min(sa.end_time, ta.end_time)
                        if overlap_start < overlap_end:
                            common_slots += 1
            if common_slots >= req.hours_per_week:
                teacher_matches.append({'teacher': teacher, 'common_slots': common_slots})

        matching_results.append({
            'requirement': req,
            'matches': teacher_matches,
        })

    return render(request, 'tutoring/admin_matching.html', {'matching_results': matching_results})
