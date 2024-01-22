from django.urls import path
from . import views

app_name = 'exams_results'

urlpatterns = [
    path('result_upload', views.UploadResultView.as_view(), name='result_upload'),
    path('results', views.ResultView.as_view(), name='result'),
]
