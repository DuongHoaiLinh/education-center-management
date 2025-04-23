from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Class(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey('Teacher', on_delete=models.SET_NULL, null=True)
    schedule = models.TextField()

class Subject(models.Model):
    name = models.CharField(max_length=100)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    class_group = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)

class Attendance(models.Model):
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    score = models.FloatField()

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid'), ('overdue', 'Overdue')])
    payment_date = models.DateField(null=True, blank=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_amount = self.amount - self.discount
        super().save(*args, **kwargs)

class Salary(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonuses = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2)
    calculation_date = models.DateField()
    days_off = models.IntegerField(default=0)
    classes_taught = models.IntegerField(default=0)
    subjects_taught = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total_salary = self.base_salary + self.bonuses - self.deductions
        super().save(*args, **kwargs)

class AbsenceRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)