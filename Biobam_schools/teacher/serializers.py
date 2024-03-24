from rest_framework import serializers
from . models import *
from registration . serializers import UserSerializer

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = "__all__"

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    designation = DesignationSerializer(read_only=True)
    expertise = SubjectSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Teacher
        fields = "__all__"