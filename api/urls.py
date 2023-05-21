from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import (
    UserRegister,
    LogoutView,
    ProfileListView,
    ProfileDetailView,
    UserView,
    UserDetailView,
    EngineerRegister,
    EngineerDetailView,
    EngineerList,
)

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegister.as_view(), name="register"),
    path("register/engineer/", EngineerRegister.as_view(), name="engineer-register"),
    path("engineer/<str:id>/", EngineerDetailView.as_view(), name="engineer-detail"),
    path("engineers/", EngineerList.as_view(), name="engineers"),
    # path(
    #     "email-verify/<str:uidb64>/<str:token>/",
    #     VerifyEmailView.as_view(),
    #     name="email-verify",
    # ),
    path("me/<str:id>/", UserDetailView.as_view(), name="me-detail"),
    path("profile/<str:user>/", ProfileDetailView.as_view(), name="profile"),
    path("users/", UserView.as_view(), name="users"),
    path("profiles/", ProfileListView.as_view(), name="profiles"),
]
