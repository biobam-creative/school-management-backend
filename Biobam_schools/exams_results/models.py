from django.db import models
from students.models import Student
from teacher.models import Subject
from admin_tools.models import *
from django.template.defaultfilters import slugify


class TermlyReportCard(models.Model):

    title = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    first_ca = models.PositiveIntegerField()
    second_ca = models.PositiveIntegerField()
    third_ca = models.PositiveIntegerField()
    exam = models.PositiveIntegerField(default=0)
    total = models.PositiveIntegerField(default=0)
    remark = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=100, blank=True)
    term_report_card = models.ForeignKey(
        TermlyReportCard, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(blank=True, unique=True,
                            max_length=200, null=True)

    def __str__(self):
        name = f'{self.term} {self.subject} result for {self.student}'
        return name

    def save(self, *args, **kwargs):
        name = f'{self.term} {self.subject} result for {self.student}'
        self.slug = slugify(name)
        super(Result, self).save(*args, **kwargs)

class ResultPdf(models.Model):
    title = models.CharField(max_length=50, unique=True)
    pdf_file = models.FileField(upload_to='results/pdfs')

    def __str__(self):
        return(self.title)

class Csv(models.Model):
    csv = models.FileField(upload_to='media/csvs')        
