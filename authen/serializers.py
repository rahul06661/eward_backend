from rest_framework import serializers
from .models import *


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

    