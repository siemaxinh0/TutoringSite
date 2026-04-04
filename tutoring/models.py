from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    role_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.role_name


class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, default='')
    is_email_verified = models.BooleanField(default=False)
    lesson_balance = models.IntegerField(default=0)
    roles = models.ManyToManyField(Role, blank=True, related_name='users')
    subjects = models.ManyToManyField(Subject, blank=True, related_name='teachers')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Availability(models.Model):
    DAYS_OF_WEEK = [
        (0, 'Poniedziałek'),
        (1, 'Wtorek'),
        (2, 'Środa'),
        (3, 'Czwartek'),
        (4, 'Piątek'),
        (5, 'Sobota'),
        (6, 'Niedziela'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        verbose_name_plural = 'availabilities'
        ordering = ['day_of_week', 'start_time']

    def __str__(self):
        return f"{self.user} : {self.get_day_of_week_display()} {self.start_time} - {self.end_time}"


class Lesson(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_lessons')
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='teacher_lessons')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    scheduled_start = models.DateTimeField()
    scheduled_end = models.DateTimeField()
    status = models.CharField(max_length=30, default='scheduled')

    def __str__(self):
        return f"Lesson: {self.subject} | {self.student} -> {self.teacher} ({self.status})"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    lessons_added = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='pending')
    provider_transaction_id = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.pk} - {self.user} - {self.amount} ({self.status})"
