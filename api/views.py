from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, response, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import (
    UserSerializer,
    LogoutSerializer,
    ProfileSerializer,
    EngineerSerializer,
)
from api.models import Profile
from api.permissions import IsUser, MeUser

User = get_user_model()


class UserRegister(APIView):
    def post(self, request: Request, format: str = "json") -> Response:
        serializer = UserSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)


class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    lookup_field = "id"
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsUser,
    ]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response(
            {"message": "User deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class EngineerRegister(APIView):
    def post(self, request, format="json"):
        serializer = EngineerSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response = serializer.data
        response["refresh"] = str(refresh)
        response["access"] = str(refresh.access_token)

        return Response(response, status=status.HTTP_201_CREATED)


class EngineerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EngineerSerializer
    lookup_field = "id"
    queryset = User.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsUser,
    ]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response(
            {"message": "Engineer deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class EngineerList(generics.ListAPIView):
    """
    See the engineers
    """

    serializer_class = EngineerSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return User.objects.filter(is_engineer=True)


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):  # type:ignore[no-untyped-def]

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


# class VerifyEmailView(GenericAPIView):
#     serializer_class = VerifyEmailSerializer

#     def patch(
#         self, request: Request, uidb64: str, token: str, **kwargs: str
#     ) -> Response:
#         data = {"uidb64": uidb64, "token": token}

#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response("Email verified", status=status.HTTP_200_OK)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = ProfileSerializer
    lookup_field = "user"
    queryset = Profile.objects.all()


class ProfileListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated,)
