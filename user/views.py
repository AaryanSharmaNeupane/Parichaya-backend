from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import views, generics

from user.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class HelloAPI(views.APIView):

    """Test api view"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        test_message = {'title': "List of api routes",
                        'routes': [
                            "api/",
                            "api/user/create",
                            "api/token",
                            "api/token/refresh",
                            "api/me",
                            "api/documents",
                            "api/documents"

                        ]}
        return Response(test_message, status=status.HTTP_200_OK)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Allow authenticated users to view and update user details"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
