from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('signup', views.TeacherSignup.as_view(), name='teacher_signup'),

]