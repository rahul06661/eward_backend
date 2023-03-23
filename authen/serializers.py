from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        
        fields = ['email', 'firstname', 'lastname', 'voter_id', 'job']


from django.contrib.auth.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    