# serializers.py
from rest_framework import serializers
from database.models import Courses


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'
