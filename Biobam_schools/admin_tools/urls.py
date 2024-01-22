from django.urls import path
from . import views

app_name = 'admin_tools'

urlpatterns = [
    path('term', views.TermView.as_view(), name='term_view'),
    path('termly_school_fee', views.SchoolFeeCreate.as_view()),
]