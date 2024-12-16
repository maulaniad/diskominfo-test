# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from database.models import Courses

from .serializers import CourseSerializer


class CoursesView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                course = Courses.objects.get(pk=pk)
                serializer = CourseSerializer(course)
                return Response(serializer.data)
            except Courses.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            courses = Courses.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            course = Courses.objects.get(pk=pk)
            serializer = CourseSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Courses.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            course = Courses.objects.get(pk=pk)
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Courses.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
