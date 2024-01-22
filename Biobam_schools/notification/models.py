from django.db import models
from registration.models import UserAccount
# Create your models here.


class Notice(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField()
    date = models.DateField(auto_now_add=True)
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
