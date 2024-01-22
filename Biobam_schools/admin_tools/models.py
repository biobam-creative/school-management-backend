from django.db import models

from teacher.models import Teacher
#from .utilities import add_school_fee


class StudentClass(models.Model):
    name = models.CharField(max_length=255, unique=True)
    arm = models.CharField(max_length = 1, blank=True, null=True)
    nickname = models.CharField(max_length = 50, blank=True, null=True)
    class_teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, blank=True, null=True)

    def nickname(self):
        if not self.nickname:
            return ""
        return self.nickname

    def __str__(self):
        return f"{self.name}{self.arm}"


class AcademicSession(models.Model):
    year = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return '{} - {}'.format(self.year, self.year + 1)


class Term(models.Model):
    number = models.PositiveIntegerField(unique=True)
    session = models.ForeignKey(
        AcademicSession, on_delete=models.CASCADE, default=None, null=True, blank=True)

    class Meta:
        ordering = ['number', ]

    def __str__(self):
        if self.number%3 == 1:
            return f'1st term {self.session}'
        elif self.number%3 == 2:
            return f'2nd term {self.session}'
        if self.number%3 == 0:
            return f'3rd term {self.session}'

class SchoolFee(models.Model):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=10000)
    
    def __str__(self):
        return f'fee for {self.term} {self.student_class}' 

