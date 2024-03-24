from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns = [
    path('signup', views.TeacherSignup.as_view(), name='teacher_signup'),
    path('teachers', views.GetTeachers.as_view(), name='teacher_list'),
    path('designations', views.GetDesignations.as_view(), name='designations'),
    path('subjects', views.GetSubjects.as_view(), name='subjects'),
    path('<id>', views.TeacherProfile.as_view(), name='teacher_profile'),
    
]