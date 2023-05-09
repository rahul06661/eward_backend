from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager



class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email=models.EmailField(unique=True,max_length=100,null=False)
    utype=models.CharField(max_length=4,null=False,blank=False)
    session_token=models.CharField(max_length=10,default='0')
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    REQUIRED_FIELDS=[]
    USERNAME_FIELD='email'
    username=None
    first_name=None
    last_name=None
    objects = CustomUserManager()

class Member(models.Model):
    email = models.EmailField(max_length=254, unique=True,null=False,primary_key=True)
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    age=models.CharField(max_length=3)   
    gender= models.CharField(max_length=3)
    phone =models.CharField(max_length=12)
    blood_group=models.CharField(max_length=3)
    ward = models.CharField(max_length=3,unique=True)
    

    def __str__(self):
        return self.email

class Users(models.Model):
    member_email=models.ForeignKey(Member,on_delete=models.CASCADE)
    email=models.EmailField(unique=True,max_length=100,null=False,default=0,primary_key=True)
    firstname=models.CharField(max_length=20)
    lastname=models.CharField(max_length=20)
    voter_id=models.CharField(max_length=20,unique=True)
    job=models.CharField(max_length=20)
    tax_payer=models.CharField(max_length=5)
    age=models.IntegerField()
    gender= models.CharField(max_length=3)
    phone =models.CharField(max_length=12)
    blood_group=models.CharField(max_length=3)
    ward = models.CharField(max_length=3)
    housenumber = models.CharField(max_length=3) 
    qualification=models.CharField(max_length=100,null=True)
    approval=models.BooleanField(default=False)
   