from django.db import models
from teacher.models import Subject, Teacher
from admin_tools.models import StudentClass

class LessonNote(models.Model):
    topic = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    body = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic