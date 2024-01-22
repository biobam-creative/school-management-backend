from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from .models import Student
from .serializers import StudentSerializer

from admin_tools.models import *
from finance.models import*


User = get_user_model()
class StudentSignup(APIView):
    def post(self, request, format=None):
        user = request.user
        data = self.request.data
        files = request.FILES


        email = data['email']
        password = data['password']
        password2 = data['password2'] 
        first_name = data['first_name']
        last_name = data['last_name']
        photo = files['photo']
        date_of_birth = data['date_of_birth']
        registration_number = data['registration_number']
        student_class = data['student_class']
        # term_id = data['term_id']
        year_of_addmission = data['year_of_addmission']
        mobile = data['mobile']
        guardian_mobile = data['guardian_mobile']

        student_class = StudentClass.objects.get(id=int(student_class))
        # term = Term.objects.get(id=term_id)
        # ac_session = AcademicSession.objects.get(year=ac_session)

        if not user.is_superuser:
            return Response({'error':'unauthorized'})
        else:
            if password == password2:
                if User.objects.filter(email=email).exists():
                    return Response({'error':'User already exist'})
                else:
                    if len(password) < 6:
                        return Response({'error':'Password is too short'})
                    else:
                        user = User.objects.create_user(email=email, password=password, name=last_name)
                        user.save()

                        student = Student.objects.create(user=user, first_name=first_name, last_name=last_name, photo=photo,
                        date_of_birth=date_of_birth,registration_number=registration_number, student_class=student_class,
                        year_of_addmission=year_of_addmission, mobile=mobile, guardian_mobile=guardian_mobile)

                        SchoolFeeBalance.objects.create(student=student, balance=0)
                        return Response({'success':'Registered sucessfully'})
            else:
                return Response({'error':'Password do not match'})
