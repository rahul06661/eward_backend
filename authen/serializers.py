from rest_framework import serializers
from .models import *
from .models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ("email",)

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        min_length=1,
    )

    class Meta:
        field = ("password")

    def validate(self, data):
        """
        Verify token and encoded_pk and then set new password.
        """
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError("Missing data.")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = CustomUser.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("The reset token is invalid")

        user.set_password(password)
        user.save()
        return data



class MemberSerializer (serializers.ModelSerializer):
    class Meta:
        model=Member
        fields = ['email', 'firstname', 'lastname', 'gender','age','ward','phone','blood_group']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        
        fields = ['email', 'firstname', 'lastname', 'phone', 'housenumber','job']


from django.contrib.auth.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    