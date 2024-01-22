from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.Payment.as_view(), name='student_payment_info'),

]
