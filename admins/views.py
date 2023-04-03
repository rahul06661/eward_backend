from django.shortcuts import render
from django.http import JsonResponse



def registermember(request):
    if request.method=="POST":
        utype=request.POST['utype']
        if utype=="admin":
            email=request.POST['email']
            firstname=request.POST['firstname']
            lastname=request.POST['lastname']
            gender=request.POST['gender']
            age=request.POST['age']
            phone=request.POST['phone']
            ward

            
        else:
            return JsonResponse({"msg":"not admin"})



def getmembers(request):
    if request.method=="POST":
        utype=request.POST['utype']
        if utype=="admin":
            pass
        else:
            return JsonResponse({"msg":"not admin"})

