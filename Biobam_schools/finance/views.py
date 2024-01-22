from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import PaymentInfoSerilalizer
from .models import SchoolFeeBalance, StudentPaymentInfo

# Create your views here.


class Payment(APIView):
    def post(self, request, format=None):
        data = request.data
        user = request.user

        amount = data['amount']

        if user.student:
            serializer = PaymentInfoSerilalizer(data)
            if serializer.is_valid():
                serializer.save()

                school_fee_balance = SchoolFeeBalance.objects.get(student=user.student)
                school_fee_balance.balance -= amount
                
                return Response(serializer.data)
            
        else:
            return Response({'error':'You must login as a student to make a payment'})
