from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
User = get_user_model()
from django.http import HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions, status

from .serializers import UserSerializer, UserSerializerWithToken, MyTokenObtainPairSerializer, LoginSerializer

from students.models import Student
from teacher.models import Teacher

from students.serializers import StudentSerializer
from teacher.serializers import TeacherSerializer


class SignupView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data

        name = data['name']
        email = data['email']
        password = data['password']
        password2 = data['password2'] 

        if password == password2:
            if User.objects.filter(email=email).exists():
                return Response({'error':'User already exist'})
            else:
                if len(password) < 6:
                    return Response({'error':'Password is too short'})
                else:
                    user = User.objects.create_user(email=email, password=password, name=name)
                    user.save()
                    return Response({'success':'User created sucessfully'})
        else:
            return Response({'error':'Password do not match'})
        


class MyObtainTokenPairWithView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']

        user = authenticate(email=email, password=password)

        try:
            teacher = Teacher.objects.get(user=user)
            teacher_serializer = TeacherSerializer(teacher).data
        except:
            teacher_serializer = ''
        try:
            student = Student.objects.get(user=user)
            student_serializer = StudentSerializer(student).data
        except:
            student_serializer = ''
            


        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            refresh = RefreshToken.for_user(user)
            print(user.is_superuser)
            print(user.is_staff)

            data = {
                'refresh':str(refresh),
                'access':str(refresh.access_token),
                'is_superuser':user.is_superuser,
                'is_staff':user.is_staff,
                'teacher':teacher_serializer,
                'student':student_serializer,
                'email':user.email
            }
            return Response(data)

        
        return Response({
            'message':'something went wrong',
            'data':serializer.errors
        })


class Dashboard(APIView):
    def get(self, request):
        students = Student.objects.all().count()
        teachers = Teacher.objects.all().count()
        data = {"students":students,"teachers":teachers}
        # serializer = UserSerializer(students, many=True)
        message ='this is the dashboard'
        return Response(data)