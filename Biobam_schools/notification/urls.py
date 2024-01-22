from django.urls import path
from . import views

#app_name = 'notification'

urlpatterns = [
    path('notifications', views.NotificationView.as_view(), name='notification'),
    path('all_notifications', views.NoticeListView.as_view(),
         name='all_notifications'),
]
