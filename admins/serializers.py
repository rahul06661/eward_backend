from authen.models import Member
from rest_framework import serializers

class MemberSerializer (serializers.ModelSerializer):
    class Meta:
        model=Member
        fields = ['email', 'firstname', 'lastname', 'gender','age','ward','phone','blood_group','password']