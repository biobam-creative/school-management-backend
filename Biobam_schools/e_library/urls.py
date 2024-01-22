from django.urls import path
from . import views

app_name = 'e_library'

urlpatterns = [
    path('book_add', views.BookUpload.as_view(), name='book_add'),
    path('books', views.BookList.as_view(), name='books'),

]
