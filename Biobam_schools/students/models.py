from django.db import models
from registration.models import UserAccount
from teacher.models import Teacher
from admin_tools.models import Term, AcademicSession, StudentClass

class Student(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='students',
                              default='studentavar.png', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    registration_number = models.CharField(max_length=6, unique=True)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, blank=True, null=True)
    year_of_addmission = models.CharField(max_length=4, blank=True, null=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    guardian_mobile = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
