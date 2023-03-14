from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer, UserSerializerProfile
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserEditProfileView(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)

        if serializer.is_valid():
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            phone_number = serializer.validated_data.get('phone_number')
            password = serializer.validated_data.get('password')
            email = serializer.validated_data.get('email')
            avatar = serializer.validated_data.get('avatar')
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if phone_number:
                user.phone_number = phone_number
            if password:
                user.password = make_password(password)
            if email:
                user.email = email
            if avatar:
                user.avatar = avatar
            user.is_host = serializer.validated_data.get('is_host', user.is_host)
            user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
