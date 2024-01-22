from django.db import models
from registration.models import UserAccount


class Designation(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Subject(models.Model):
    name = models.CharField(max_length=200)
    added_in = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

class Teacher(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    initials = models.CharField(max_length=150)

    photo = models.ImageField(upload_to='teachers',
                              default='teacheravatar.jpg')
    date_of_birth = models.DateField(blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    expertise = models.ManyToManyField(
        to=Subject, blank=True, related_name='expert_in')
    mobile = models.CharField(max_length=11, blank=True, null=True)
    joining_date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['joining_date', 'first_name']

    def __str__(self):
        return '{} {} ({})'.format(self.first_name, self.initials, self.designation)



