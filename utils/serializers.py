from rest_framework import serializers
from .models import *
from authen.models import Users

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification       
        fields = ['id','name','img_path','desc','status','created_on','update_on']

class GetwardSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields=['ward']

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model=family
        fields=['email','firstname','lastname','phone']


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comp
        fields=['id','name','desc','img_path','status','created_on','update_on']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields=['comment','user','update_on']

class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model=family
        fields=['firstname','lastname','phone','email']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=['firstname','lastname','phone','email']

class GetUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model=Users
        fields=['firstname','lastname','voter_id','job','tax_payer','age','gender','phone','blood_group','housenumber','qualification']



class GetMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model=Member
        fields=['firstname','lastname','age','gender','phone','blood_group']
  