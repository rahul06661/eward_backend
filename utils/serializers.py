from rest_framework import serializers
from .models import *

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification       
        fields = ['id','name','img_path','desc','status','created_on','update_on']

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comp
        fields=['id','name','desc','img_path','status','created_on','update_on']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comments
        fields=['comment','user','update_on']
    