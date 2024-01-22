from django.db import models
from students.models import Student
from admin_tools.models import Term, AcademicSession

# Create your models here.


class StudentPaymentInfo(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        string = f'{self.student} {self.date}'
        return string


class SchoolFeeBalance(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField()

    def __str__(self):
        string = f'{self.student} school fee balance'
        return string
