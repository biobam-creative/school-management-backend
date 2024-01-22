from django.db import models
from admin_tools.models import StudentClass


class Book(models.Model):
    title = models.CharField(max_length=255)
    book_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, default='Mathematics')
    author = models.CharField(max_length=255)
    edition = models.CharField(max_length=255)
    year = models.CharField(max_length=10)
    image = models.ImageField(upload_to='e_library/images', blank=True)
    book = models.FileField(upload_to='e_library/pdfs', blank=True)

    def __str__(self):
        return f'{self.title} for {self.book_class}'
