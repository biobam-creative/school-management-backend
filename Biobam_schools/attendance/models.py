from django.db import models
from students.models import Student

# Create your models here.
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date =  models.DateField()
    morning = models.BooleanField()
    afternoon = models.BooleanField()
    late = models.BooleanField()

    def __str__(self):
        return f'{self.student} {self.date}'