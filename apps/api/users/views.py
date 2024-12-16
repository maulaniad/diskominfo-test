# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from database.models import Users
from .serializers import UserSerializer


class UserView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                user = Users.objects.get(pk=pk)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except Users.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            users = Users.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            user = Users.objects.get(pk=pk)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user = Users.objects.get(pk=pk)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
