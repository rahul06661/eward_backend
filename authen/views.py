from django.shortcuts import render
import random
from django.core.mail import send_mail
from .serializers import UserSerializer
from rest_framework.response import Response
from asgiref.sync import sync_to_async
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
import re
from .serializers import UserSerializer
from .models import Member, Users
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets, response
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from . import serializers

@csrf_exempt
def UserRegisteration(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email)
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        voter_id = request.POST['voter_id']
        job = request.POST['job']
        tax_payer = request.POST['tax_payer']
        age = int(request.POST['age'])
        gender = request.POST['gender']
        phone = request.POST['phone']
        blood_group = request.POST['blood_group']
        ward = request.POST['ward']
        housenumber = request.POST['housenumber']
        password = request.POST['password']
        qualification = request.POST['qualification']
       
        try:
            member = Member.objects.get(ward=ward)
            print("______________________________________________________")
            print(member)
        except:
            return JsonResponse({'msg': 'Registeration not allowed'})
       
        try:
            user_obj = Users(member_email=member, email=email, firstname=firstname, lastname=lastname, voter_id=voter_id, job=job,
                                tax_payer=tax_payer, qualification=qualification, age=age, gender=gender, phone=phone, blood_group=blood_group, ward=ward, housenumber=housenumber, approval=False)
            user_obj.save()
            custuserobj = CustomUser.objects.create_user(
                email=email, utype='user', password=password)
            custuserobj.save()
            return Response({'msg': 'User registerd'})
        except IntegrityError as e:
            return JsonResponse({'msg': 'error occured'})

    else:
        return Response({'msg': 'Invaild request type'})

@csrf_exempt
def RestPassword(request):
    if request.method=="POST":
        email=request.POST["email"]
        password=request.POST["password"]
        try:
            userobj=CustomUser.objects.get(email=email)
            
        except:
            return JsonResponse({'msg':"user not found"})
        #print(dir(userobj))
        userobj.set_password(password)
        userobj.save()
        return JsonResponse({'msg': 'Password Changed'})
        
@csrf_exempt
def GetMembers(request):
    if request.method == 'POST':
        user=request.POST['utype']
        if user=='admin':
            memb_obj=Member.objects.all()
            serialized_memb_obj=MemberSerializer(memb_obj,many=True)
            return JsonResponse({'data': serialized_memb_obj.data,
            'msg': 'sucess'})
        else:
            return JsonResponse({'msg': 'Not admin type'})
    else:
        return JsonResponse({'msg': 'Invaild request'})


@csrf_exempt
def MemberRegisteration(request):
    if request.method == 'POST':
        user=request.POST['utype']
        if user=='admin':
            email = request.POST['email']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            age = request.POST['age']
            gender = request.POST['gender']
            phone = request.POST['phone']
            blood_group = request.POST['blood_group']
            ward = request.POST['ward']
            password = 'Rahul@98'
            try:               
                Member_obj = Member(email=email, firstname=firstname, lastname=lastname, age=age,
                                gender=gender, phone=phone, blood_group=blood_group, ward=ward)
                Member_obj.save()
                custuserobj = CustomUser.objects.create_user(
                email=email, utype='memb', password=password)
                custuserobj.save()
                subject="welcome"
                message="Your default password is : Rahul@98"
                email_from=settings.EMAIL_HOST_USER
                recipient_list=[email]
                send_mail(subject,message,email_from,recipient_list)
                return JsonResponse({'msg': 'Member registerd'})
            except IntegrityError:
                return JsonResponse({'msg': 'Already Registered'})           
        else:
            return JsonResponse({'msg': 'not Admin'})
    else:
            return JsonResponse({'msg': 'Invaild request type'})


@csrf_exempt
def singin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        
        try:
            user = authenticate(email=username, password=password)
            if user is not None:
                user_dicts = CustomUser.objects.filter(
                    email=username).values().first()

                if user_dicts['utype'] != 'memb':
                    if not (Users.objects.get(email=username).approval):
                        return JsonResponse({'error': 'Account not verified'})
                user_dicts.pop('password')
                if user.session_token != "0":
                    user.session_token = "0"
                    user.save()
                    return JsonResponse({"error": "previous session exists"})
                token = generatetoken()
                user.session_token = token
                user.save()
                login(request, user)
                return JsonResponse({'token': token, 'user': user_dicts})
            else:
                return JsonResponse({'error': 'Invalid Credentials'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Invalid Credentials'})


@csrf_exempt
def approve(request):
    if request.method == 'POST':
        email = request.POST['email']
        print()
        print(email)
        user_obj = Users.objects.filter(email=email).first()
        user_obj.approval = '1'
        user_obj.save()
        return JsonResponse({'msg': 'sucess'})
    else:
        return JsonResponse({'msg': 'fail'})


@csrf_exempt
def list_users_not_approved(request):
    if request.method == 'POST':
        utype = request.POST['utype']
        if utype == "memb":
            email = request.POST['email']
            print(email)
            user_obj = Users.objects.filter(approval='0', member_email=email)
            serializer = UserSerializer(user_obj, many=True)
            print(serializer.data)
            if user_obj is not None:
                print(serializer.data)
                return JsonResponse({"data": serializer.data,
                                     'msg': 'sucess'})
            else:
                return JsonResponse({"data": []})
        else:
            return JsonResponse({'msg': 'Invaild message'})
    else:
        return JsonResponse({'msg': 'Invaild request'})


@csrf_exempt
def list_users_approved(request, id):
    if request.user.is_authenticated:
        if request.user.utype == "memb":
            if request.method == 'POST':
                user_obj = Users.objects.filter(approval=1, member_id=id)
                serializer = UserSerializer(user_obj, many=True)
                if user_obj is not None:
                    print(user_obj)
                    return JsonResponse({"data": serializer.data})
                else:
                    return JsonResponse({'msg': 'no users'})
            else:
                return JsonResponse( {'error': 'Invaild message'})
        else:
            return JsonResponse({'error': 'Not Memberuser'})
    else:
        return JsonResponse({'error': 'Not autheticated'})


def signout(request, id):
    logout(request)
    usermodel = get_user_model()
    try:
        user = usermodel.objects.get(id=id)
        user.session_token = '0'
        user.save()
    except:
        return JsonResponse({'error': 'user id'})
    return JsonResponse({'msg': 'sucess'})


def generatetoken():
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in range(10))



@csrf_exempt
def PasswordReset(request):
    if request.method=="POST":
        email = request.POST['email']
        user = CustomUser.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse(
                "reset-password",
                kwargs={"encoded_pk": encoded_pk, "token": token},
            )
            current_ip=request.get_host()
            reset_link = f"{current_ip}{reset_url}"
            subject="password Reset Link"
            message=reset_link
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[email]
            send_mail(subject,message,email_from,recipient_list)
            return JsonResponse({
                    "message": 
                    "Password Resetting link shared"})         
        else:
            return JsonResponse({"message": "User doesn't exists"})
@csrf_exempt          
def reset_password(request, *args, **kwargs):   
    if request.method=="POST":
        password=request.POST.get("password")    
        token = kwargs.get('token')
        encoded_pk = kwargs.get('encoded_pk')
        if token is None or encoded_pk is None:
            raise 'error'
        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = CustomUser.objects.get(pk=pk)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError('The reset token is invalid')       
        user.set_password(password)
        user.save()
        return JsonResponse({'message': 'Password reset complete'}, status=status.HTTP_200_OK)
    else:
        return render(request, 'password_change.html')



class ResetPasswordAPI(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)
        return response.Response(
            {"message": "Password reset complete"},
            status=status.HTTP_200_OK,
        )
