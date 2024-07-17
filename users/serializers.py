from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers

from Videoflix import settings
from users.models import CustomUser
from django.urls import reverse


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'username', 'first_name']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            username=validated_data['email']
        )
        return user


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email address.")
        return value

    def save(self):
        request = self.context.get('request')
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(
            reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        )
        email_body = f'Hi {user.email},\nPlease use this link to reset your password:\n{reset_link}'
        send_mail(
            'Reset your password',
            email_body,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )


class ConfirmPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    def save(self, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            self.user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            raise serializers.ValidationError('Your token or the user doesn´t exist.')

        if not default_token_generator.check_token(self.user, token):
            raise serializers.ValidationError('Invalid token')

        self.user.set_password(self.validated_data['new_password'])
        self.user.save()
