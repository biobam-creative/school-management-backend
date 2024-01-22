from django.shortcuts import render


# Create your views here.

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import NoticeSerializer, NoticeViewSerializer
from .models import Notice


class NotificationView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = request.data
        user = request.user

        serializer = NoticeSerializer(data=data)

        if serializer.is_valid():
            serializer.save(sender=user)
            return Response(serializer.data)


class NoticeListView(ListAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeViewSerializer
