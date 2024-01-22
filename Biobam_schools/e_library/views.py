from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import BookSerializer
from .models import Book

# Create your views here.


class BookUpload(APIView):

    def post(self, request, format=None):
        data = request.data
        files = request.FILES
        
        title = data['title']
        book_class = data['book_class']
        subject = data['subject']
        author = data['author']
        edition = data['edition']
        year = data['year']
        image = files['image']
        book = files['book']

        data = {
            'title':title,
            'book_class':book_class,
            'subject':subject,
            'author':author,
            'edition':edition,
            'year':year,
            'image':image,
            'book':book
        }
        serializer = BookSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({'Error':'Invalid Data'})


class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
