from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, Subject, Availability, Lesson, Payment

class CustomUserAdmin(UserAdmin):
    # 1. Co ma być widać w głównej tabeli (tej ze screena)
    list_display = ('username', 'email', 'first_name', 'last_name', 'lesson_balance', 'is_staff')
    
    # 2. Co ma być widać, gdy klikniesz w konkretnego użytkownika, żeby go edytować
    fieldsets = UserAdmin.fieldsets + (
        ('Nasze dodatkowe dane z Vertabelo', {
            'fields': ('phone_number', 'lesson_balance', 'roles', 'subjects', 'is_email_verified',),
        }),
    )

# Wyrejestrowujemy standardowy widok (jeśli był) i rejestrujemy nasz nowy
admin.site.register(User, CustomUserAdmin)

# Reszta zostaje bez zmian
admin.site.register(Role)
admin.site.register(Subject)
admin.site.register(Availability)
admin.site.register(Lesson)
admin.site.register(Payment)