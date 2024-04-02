from django.contrib.auth import get_user_model
# from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import permissions
from rest_framework import status

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
        password2 = data['confirmPassword'] 
        first_name = data['firstName']
        initials = data['initials']
        photo = data['photo']
        date_of_birth = data['dateOfBirth']
        designation = data['designation']
        expertise = data['expertise'].split(',')
        mobile = data['phone']
        joining_date = data['joiningDate']

        try:
            designation = Designation.objects.get(title=designation)
        except Designation.DoesNotExist:
            return Response({'error':'not found' }, status=status.HTTP_404_NOT_FOUND)

        expertises = []
        for i in expertise:
            try:
                expertise = Subject.objects.get(name=i)
                expertises.append(expertise)
            except Subject.DoesNotExist:
                return Response({'error':'not found' }, status=status.HTTP_404_NOT_FOUND)

        if not user.is_superuser:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if password == password2:
                if User.objects.filter(email=email).exists():
                    return Response({'error':'User already exist'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    if len(password) < 6:
                        return Response({'error':'Password is too short'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    else:
                        user = User.objects.create_user(email=email, password=password, name=first_name)
                        user.is_staff=True
                        user.save()
                        teacher = Teacher.objects.create(user=user, first_name=first_name, initials=initials, photo=photo,
                        date_of_birth=date_of_birth,designation=designation,
                        mobile=mobile, joining_date=joining_date)

                        print(expertises)
                        for expertise in expertises:
                            
                            teacher.expertise.add(expertise)

                        return Response({'success':'Registered sucessfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error':'Password do not match'}, status=status.HTTP_401_UNAUTHORIZED)

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