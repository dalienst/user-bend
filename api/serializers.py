from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from api.token import account_activation_token
from userapp.settings import EMAIL_USER

from api.validators import (
    validate_password_digit,
    validate_password_lowercase,
    validate_password_symbol,
    validate_password_uppercase,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer of the user model
    User is able to create an account
    An instance of Profile is created once the user registers
    """

    id = serializers.CharField(
        read_only=True,
    )

    username = serializers.CharField(
        max_length=20,
        min_length=4,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )

    class Meta:
        model = User
        fields = ("id", "email", "username", "password")
        read_only_fields = ("id", "is_verified")

    @staticmethod
    def send_email(user, request):
        current_site_info = get_current_site(request)
        email_body = render_to_string(
            "email_verification.html",
            {
                "user": user,
                "domain": current_site_info.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            }

        )
        send_mail(
            "Please Verify your email!!!",
            email_body,
            EMAIL_USER,
            [user.email],
            fail_silently=False,
        )

    def create(self, validated_data):
        request = self.context.get("request")
        user = User.objects.create_user(**validated_data)
        user.save()
        Profile.objects.create(user=user)
        self.send_email(user, request)
        return user



class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField()
    uidb64 = serializers.CharField()

    class Meta:
        fields = ("token", "uidb64")

    def validate(self, data):
        user = None
        try:
            user_id = force_str(urlsafe_base64_decode(data.get("uidb64")))
            user = User.objects.get(pk=user_id)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError(
                "Invalid user id", code="invalid_code"
            )

        token = data.get("token")
        if user and account_activation_token.check_token(user, token):
            return data

        raise serializers.ValidationError(
            "Invalid or expired token", code="invalid_token"
        )

    def save(self, **kwargs):
        user_id = force_str(
            urlsafe_base64_decode(self.validated_data.get("uidb64"))
        )
        user = User.objects.get(pk=user_id)
        user.is_verified = True
        user.save()
        return user
             


class ProfileSerializer(serializers.ModelSerializer):
    """
    The profile serializer to enable retrieval and updating of profile of the user
    """

    username = serializers.CharField(read_only=True, source="user.username")
    image = serializers.ImageField(use_url=True, required=False)
    firstname = serializers.CharField(allow_blank=True, required=False)
    lastname = serializers.CharField(allow_blank=True, required=False)
    phonenumber = serializers.IntegerField(required=False)
    location = serializers.CharField(allow_blank=True, required=False)
    dob = serializers.DateField(required=False)
    bio = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Profile
        fields = ("username", "bio", "image", "location", "firstname", "lastname", "phonenumber", "dob")

    def update(self, instance, validated_data):
        instance.bio = validated_data.get("bio", instance.bio)
        instance.image = validated_data.get("image", instance.image)
        instance.location = validated_data.get("location", instance.location)
        instance.firstname = validated_data.get("firstname", instance.firstname)
        instance.lastname = validated_data.get("lastname", instance.lastname)
        instance.phonenumber = validated_data.get("phonenumber", instance.phonenumber)
        instance.dob = validated_data.get("dob", instance.dob)
        instance.save()
        return instance


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):  # type:ignore[no-untyped-def]
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):  # type:ignore[no-untyped-def]

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:

            raise serializers.ValidationError(
                "Invalid or expired token", code="invalid_token"
            )
