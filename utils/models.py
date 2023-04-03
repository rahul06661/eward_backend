from django.db import models
from authen.models import Member,Users


class Notification(models.Model): 
    member_email=models.ForeignKey(Member,on_delete=models.CASCADE)
    name=models.CharField(max_length=20) 
    img_path=models.ImageField(upload_to='media',null=True)
    desc=models.CharField(max_length=20)
    status=models.CharField(max_length=20)
    created_on =models.DateField(auto_now_add=True)
    update_on =models.DateField(auto_now=True)  

class Comp(models.Model):
    member_email=models.ForeignKey(Member,on_delete=models.CASCADE)
    user_id=models.ForeignKey(Users,on_delete=models.CASCADE) 
    name=models.CharField(max_length=20) 
    desc=models.CharField(max_length=20) 
    img_path=models.ImageField(upload_to='media',null=True)
    status=models.CharField(max_length=20)
    remark=models.CharField(max_length=20)
    created_on =models.DateField(auto_now_add=True)
    update_on =models.DateField(auto_now=True)

class family(models.Model):
    user_id=models.ForeignKey(Users,on_delete=models.CASCADE)
    email=models.EmailField(unique=True,max_length=100,null=True)
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    voter_id=models.CharField(max_length=20)
    job=models.CharField(max_length=20)
    tax_payer=models.CharField(max_length=5)
    age=models.CharField(max_length=3)
    gender= models.CharField(max_length=3)
    phone =models.CharField(max_length=12)
    blood_group=models.CharField(max_length=3)
    qualification=models.CharField(max_length=100,null=True)
    relation=models.CharField(max_length=100,default= ' ')

