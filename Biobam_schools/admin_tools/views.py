from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import *
from .models import *

from finance.models import SchoolFeeBalance



class TermView(APIView):
    def post(self, request, format=None):
        data = request.data
        user = request.user

        year = int(data['year'])
        number = data['number']

        if user.is_superuser:
            try:
                session = AcademicSession.objects.get(year=year)
            except ObjectDoesNotExist:
                session = AcademicSession.objects.create(year=year)

                # balances = SchoolFeeBalance.objects.all()
                # for balance in balances:
                #     balance.balance += school_fee
                #     balance.save()
                Term.objects.create(number=number, session=session, school_fee=school_fee)
                return Response({'Message':'Term created successfully'})
            
        else:
            return Response({'error':'You must login as an admin.'})

class SchoolFeeCreate(APIView):
    def post(self, request, format=None):
        data = request.data
        user = request.user

        term_id = data['term_id']
        student_class_id = data['student_class_id']
        amount = data['amount']

        term = Term.objects.get(id=term_id)
        student_class = StudentClass.objects.get(id=student_class_id)

        if user.is_superuser:
            students = Student.objects.filter(student_class=student_class)
            for student in students:
                balance = SchoolFeeBalance.objects.get(student=student)
                balance.balance += amount
                balance.save()
            SchoolFee.objects.create(term=term, student_class=student_class, amount=amount)
            return Response({'Message':f'{student_class}, {term} Term school fee created successfully'})
        else:
            return Response({'error':'You must login as an admin.'})
