from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('signup', views.StudentSignup.as_view(), name='student_signup'),
    path('students/<student_class>', views.GetStudents.as_view(), name='student_class'),

]