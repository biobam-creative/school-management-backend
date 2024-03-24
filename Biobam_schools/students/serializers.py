from rest_framework import serializers
from . models import Student


class StudentSerializer(serializers.ModelSerializer):
    # student_class = PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Student
        fields = "__all__"