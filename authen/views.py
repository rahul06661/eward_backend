from django.shortcuts import render
import random
from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework.decorators import api_view
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
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .serializers import UserSerializers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


@csrf_exempt
def UserRegisteration(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email)
        # if not re.match("^[\w\,\+\-]@[\w]+\,[a-z]{2,3}$",email):
        #    return JsonResponse({'error':'Invalid Mail Address'})
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        voter_id = request.POST['voter_id']
        job = request.POST['job']
        tax_payer = request.POST['tax_payer']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        blood_group = request.POST['blood_group']
        ward = request.POST['ward']
        housenumber = request.POST['housenumber']
        password = request.POST['password']

        member = Member.objects.get(ward=ward)
        print(
            "___ ____ ______ ___ _____ ____ ____ ______ ___ _____ ___ ____ _________ _____")
        print(member)
        user_obj = Users(member_email=member, email=email, firstname=firstname, lastname=lastname, voter_id=voter_id, job=job,
                         tax_payer=tax_payer, age=age, gender=gender, phone=phone, blood_group=blood_group, ward=ward, housenumber=housenumber, password=password, approval=False)
        user_obj.save()
        custuserobj = CustomUser.objects.create_user(
            email=email, utype='user', password=password)
        custuserobj.save()
        return Response({'msg': 'User registerd'})
    else:
        return Response({'error': 'Invaild request type'})


@csrf_exempt
def MemberRegisteration(request):
    if request.method == 'POST':
        email = request.POST['email']
        # if not re.match("^[\w\,\+\-]@[\w]+\,[a-z]{2,3}$",email):
        #    return JsonResponse({'error':'Invalid Mail Address'})
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        age = request.POST['age']
        gender = request.POST['gender']
        phone = request.POST['phone']
        blood_group = request.POST['blood_group']
        ward = request.POST['ward']
        password = request.POST['password']
        Member_obj = Member(email=email, firstname=firstname, lastname=lastname, age=age,
                            gender=gender, phone=phone, blood_group=blood_group, ward=ward, password=password)
        Member_obj.save()
        custuserobj = CustomUser.objects.create_user(
            email=email, utype='memb', password=password)
        custuserobj.save()
        return JsonResponse({'msg': 'Member registerd'})
    else:
        return JsonResponse({'error': 'Invaild request type'})


@csrf_exempt
def singin(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        if len(password) < 7:
            return JsonResponse({'error': 'Invalid password'})
        try:
            user = authenticate(email=username, password=password)
            if user is not None:
                user_dicts = CustomUser.objects.filter(
                    email=username).values().first()

                if not user_dicts['utype'] == 'memb':
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
                return JsonResponse({'error': 'invalid email'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'Invalid email'})


@csrf_exempt
def list_users_not_approved(request, id):
    if request.user.is_authenticated:
        if request.user.utype == "memb":
            if request.method == 'POST':
                user_obj = Users.objects.filter(approval=0, member_id=id)
                serializer = UserSerializer(user_obj, many=True)
                print(serializer.data)
                if user_obj is not None:
                    print(user_obj)
                    return JsonResponse({"data": serializer.data})
                else:
                    return JsonResponse({})
            else:
                return JsonResponse({'error': 'Invaild message'})
        else:
            return JsonResponse({'error': 'Not Memberuser'})
    else:
        return JsonResponse({'error': 'Not autheticated'})


@permission_classes([IsAuthenticated])
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
                return JsonResponse({'error': 'Invaild message'})
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
