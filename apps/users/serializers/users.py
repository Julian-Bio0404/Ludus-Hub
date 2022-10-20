"""Users serializers."""

# Utilities
import jwt

# Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from apps.users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta options."""
        model = User
        fields = [
            'username', 'first_name',
            'last_name', 'email',
            'phone_number',
            'verified', 'role'
        ]

        read_only_fields = [
            'username', 'first_name',
            'last_name', 'email',
            'profile', 'verified'
        ]


class UserSignUpSerializer(serializers.Serializer):
    """
    User signup serializer.
    Handle sign up data validation and user creation.
    """

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    username = serializers.CharField(
        min_length=4, max_length=25,
        validators=[UniqueValidator(queryset=User.objects.all())])

    # Phone number
    phone_regex = RegexValidator(
        regex=r"^\+1?\d{1,4}[ ]\d{10}$",
        message='Phone number must be entered in the format: +99 9999999999. Up to indicative + 10 digits allowed.')

    phone_number = serializers.CharField(
        validators=[phone_regex], required=False)

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    # Role
    def role_validator(role):
        """Verify the role."""
        if role not in User.Role.values.keys():
            raise serializers.ValidationError('Role not allowed.')

    role = serializers.CharField(
        min_length=4, max_length=16, validators=[role_validator])

    def validate(self, data):
        """Verify password match and type identification."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']

        if passwd != passwd_conf:
            raise serializers.ValidationError('Password don´t match')
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Create user."""
        data.pop('password_confirmation')
        return User.objects.create_user(**data)


class UserLoginSerializer(serializers.Serializer):
    """
    User login serializer.
    Handle the login request data.
    """

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials.')

        if not user.verified:
            raise serializers.ValidationError('Account is not active yet.')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve token."""
        token, _ = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(
                data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')
        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.verified = True
        user.save()


class UpdatePasswordSerializer(serializers.Serializer):
    """Update user's password serializer."""

    old_password = serializers.CharField(
        required=True, min_length=8, max_length=64)

    password = serializers.CharField(
        required=True, min_length=8, max_length=64)

    password_confirmation = serializers.CharField(
        required=True, min_length=8, max_length=64)

    def validate(self, data):
        """Check password."""
        if not self.context['user'].check_password(data['old_password']):
            raise serializers.ValidationError('Wrong password.')

        if data['password_confirmation'] != data['password']:
            raise serializers.ValidationError('Password don´t match')
        password_validation.validate_password(data['password'])
        return data

    def save(self):
        """Update user's password."""
        user = self.context['user']
        user.set_password(self.validated_data['password'])
        user.save()
