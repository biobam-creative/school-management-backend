from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import permissions

from .models import *
from .serializers import *


User = get_user_model()
class TeacherSignup(APIView):
    def post(self, request, format=None):
        data = self.request.data
        files = request.FILES
        user = request.user

        email = data['email']
        password = data['password']
        password2 = data['password2'] 
        first_name = data['first_name']
        initials = data['initials']
        photo = files['photo']
        date_of_birth = data['date_of_birth']
        designation = data['designation']
        expertise = data['expertise']
        mobile = data['mobile']
        joining_date = data['joining_date']

        designation = Designation.objects.get(title=designation)
        expertises = Subject.objects.filter(name=expertise)

        if not user.is_superuser:
            return Response({'error': 'Unauthorized'})
        else:
            if password == password2:
                if User.objects.filter(email=email).exists():
                    return Response({'error':'User already exist'})
                else:
                    if len(password) < 6:
                        return Response({'error':'Password is too short'})
                    else:
                        user = User.objects.create_user(email=email, password=password, name=first_name)
                        user.is_staff=True
                        user.save()
                        teacher = Teacher.objects.create(user=user, first_name=first_name, initials=initials, photo=photo,
                        date_of_birth=date_of_birth,designation=designation,
                        mobile=mobile, joining_date=joining_date)

                        for expertise in expertises:
                            teacher.expertise.add(expertise)

                        return Response({'success':'Registered sucessfully'})
            else:
                return Response({'error':'Password do not match'})

class GetTeachers(APIView):
    def get(self,request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

class TeacherProfile(APIView):
    def get(self, request, id):
        teacher =  Teacher.objects.get(id=id)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)


class GetDesignations(ListAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer

class GetSubjects(ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer