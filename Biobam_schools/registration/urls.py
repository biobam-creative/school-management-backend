from django.urls import path
from .views import SignupView, MyObtainTokenPairWithView, LoginView, Dashboard

urlpatterns = [
     path('signup', SignupView.as_view()),
     path('token/obtain', LoginView.as_view()),
     path('dashboard', Dashboard.as_view()),

 ]