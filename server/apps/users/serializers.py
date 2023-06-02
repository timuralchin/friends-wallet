from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from server.apps.users.models import User


class TokensPairSerializer(serializers.Serializer):
    """Jwt tokens pair serializer."""

    access = serializers.CharField(max_length=500)
    refresh = serializers.CharField(max_length=500)


class RegistrationSerializer(serializers.Serializer):
    """User registration serializer."""

    email = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(
        label=_('Password'),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        validators=[validate_password],
    )


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name')


class AuthenticatedUserSerializer(serializers.Serializer):
    """Authenticated user serializer."""

    user = UserSerializer()
    tokens = TokensPairSerializer()


class LogoutSerializer(serializers.Serializer):
    """User logout serializer."""

    refresh = serializers.CharField()
