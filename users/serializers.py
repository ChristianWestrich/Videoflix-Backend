from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMultiAlternatives
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
            raise serializers.ValidationError("No user with this email address exists.")
        return value

    def save(self):
        request = self.context.get('request')
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        frontend_uri = "http://localhost:4200/password_confirm"
        reset_link = f"{frontend_uri}/uidb64={uid}/token={token}"

        email_subject = 'Reset your password for Videoflix'
        email_body_text = f'Hi {user.email},\n\nPlease use this link to reset your password:\n\n{reset_link}'
        email_body_html = f'''
            <p>Hi
             <h2>{user.email},</h2></p>
            <p>Please use the following link to reset your password:</p>
           <p><a href="{reset_link}" style="display: inline-block; padding: 15px 25px; font-size: 24px; color: white; background-color: red; border: 1px solid white; border-radius: 30px; text-decoration: none;">Reset Password</a></p>
        '''

        msg = EmailMultiAlternatives(email_subject, email_body_text, settings.EMAIL_HOST_USER, [user.email])
        msg.attach_alternative(email_body_html, "text/html")
        msg.send()


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
