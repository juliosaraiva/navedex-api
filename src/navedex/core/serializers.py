from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=8, write_only=True
    )
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')

    def validate(self, attrs):
        email = attrs.get("email", None)
        check_user = get_user_model().objects.filter(email=email).exists()
        if check_user:
            raise serializers.ValidationError("Email Already Exists")
        return attrs

    def create(self, validate_data):
        return get_user_model().objects.create_user(**validate_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'token')

    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)

        if email is None:
            msg = _("An email address is required to log in")
            raise serializers.ValidationError(msg, code="authentication")

        if password is None:
            msg = _("A password is required to log in")
            raise serializers.ValidationError(msg, code="authentication")

        user = authenticate(
            email=email,
            password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code='authentication')

        return {
            "email": user.email,
            "token": user.token
        }
