from django.contrib.auth import get_user_model
from .models import Notification, Comp, family, Comments
from authen.models import Users, Member
from authen.models import CustomUser
from django.http import JsonResponse
from .serializers import *
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_complaint_chat(request):
    if request.method == "POST":
        complaint_ids = request.POST['id']
        com_obj = Comp.objects.get(id=complaint_ids)
        comet_obj = Comments.objects.filter(complaint_id=com_obj)
        serialobj = CommentSerializer(comet_obj, many=True)

        return JsonResponse({'messages': serialobj.data,
                             'msg': 'sucess'})
    else:
        return JsonResponse({'msg': 'error occured'})


@csrf_exempt
def get_notification(request):
    if request.method == "POST":
        utype = request.POST['utype']
        token = request.POST['token']
        obj = CustomUser.objects.get(session_token=token)
        if obj is not None:
            if utype == 'user':
                mem_email = Users.objects.get(email=obj).member_email
            elif utype == 'memb':
                mem_email = Member.objects.get(email=obj).email
            noti_obj = Notification.objects.filter(member_email=mem_email)
            serializer = NotificationSerializer(noti_obj, many=True)
            return JsonResponse({'notifications': serializer.data,
                                 'msg': 'sucess'})
        else:
            return JsonResponse({'error': 'error occured'})
    else:
        return JsonResponse({'error': 'Invaild Request or user not Authenticated'})


@csrf_exempt
def get_complaint(request):
    if request.method == "POST":
        utype = request.POST['utype']
        token = request.POST['token']
        obj = CustomUser.objects.get(session_token=token)
        
        if obj is not None:
            if utype == 'memb':
                member_obj = Member.objects.get(email=obj)
                comp_obj = Comp.objects.filter(member_email=member_obj)
            elif utype == 'user':
                user_obj = Users.objects.get(email=obj)               
                memb_obj=Member.objects.get(email=user_obj.member_email)
                comp_obj = Comp.objects.filter(member_email=memb_obj)
            serializer = ComplaintSerializer(comp_obj, many=True)
            return JsonResponse({'complaints': serializer.data,
                                 'msg': 'sucess'})
        else:
            return JsonResponse({'error': 'error occured'})
    else:
        return JsonResponse({'error': 'Invaild Request or user not Authenticated'})


@csrf_exempt
def post_complaint(request):
    if request.method == "POST":
        img_path = " "
        utype = request.POST['utype']
        token = request.POST['token']
        if utype == 'user':
            obj = CustomUser.objects.get(session_token=token)
            if obj is not None:
                user_obj = Users.objects.get(email=obj)
                member_obj = Member.objects.get(ward=user_obj.ward)
                name = request.POST['name']
                desc = request.POST['desc']
                try:
                    img_path = request.FILES['img_path']
                except:
                    print("error occuerd")
                status = '1'
                comp_obj = Comp(member_email=member_obj, user_id=user_obj,
                                name=name, desc=desc, img_path=img_path, status=status)
                comp_obj.save()
                return JsonResponse({'sucess': 'complaint registerd'})
            else:
                return JsonResponse({'error': ' complaint not registerd'})
        else:
            return JsonResponse({'error': 'Not user type'})
    else:
        return JsonResponse({'error': 'Invaild Request'})


@csrf_exempt
def analysis(request):
    if request.method == "POST":
        data_dict = []
        selectedData = request.POST['selectedData']
        selectedItem = request.POST['selectedItem']
        user = request.POST['user']
        memb_obj = Member.objects.get(email=user)
        user_objs = Users.objects.filter(member_email=memb_obj)

        if user_objs is not None:
            if selectedData == "Age":
                ages = selectedItem.split('-')
                age1 = int(ages[0])
                age2 = int(ages[1])
                user_objs_data = Users.objects.filter(member_email=memb_obj).filter(age__gt=age1,age__lte=age2 )
                serializers_user = UserSerializer(user_objs_data, many=True)
                data_dict = data_dict+serializers_user.data
                for objs in user_objs:
                    fam_data_obj = family.objects.filter(
                                user_id=objs).filter(age__gt=ages[0],age__lte=ages[1] )
                    serializers_fam = FamilySerializer(
                                fam_data_obj, many=True)
                    data_dict = data_dict+serializers_fam.data
                return JsonResponse({'data': data_dict,
                                        'msg': 'sucess'})
            elif selectedData== "Job":
                print("cdscdscscsdc")
                user_objs_data = Users.objects.filter(member_email=memb_obj).filter(job=selectedItem)
                serializers_user = UserSerializer(user_objs_data, many=True)
                data_dict = data_dict+serializers_user.data
                print(selectedItem)
                print(selectedData)
                print(data_dict)

                for objs in user_objs:
                    fam_data_obj = family.objects.filter(
                        user_id=objs).filter(job=selectedItem)
                    serializers_fam = FamilySerializer(
                        fam_data_obj, many=True)
                    data_dict = data_dict+serializers_fam.data
                return JsonResponse({'data': data_dict,
                                    'msg': 'sucess'})
            elif selectedData == "Qualification":
                user_objs_data = Users.objects.filter(member_email=memb_obj).filter(qualification=selectedItem)
                serializers_user = UserSerializer(user_objs_data, many=True)
                data_dict = data_dict+serializers_user.data

                for objs in user_objs:
                    fam_data_obj = family.objects.filter(
                        user_id=objs).filter(qualification=selectedItem)
                    serializers_fam = FamilySerializer(
                        fam_data_obj, many=True)
                    data_dict = data_dict+serializers_fam.data
                return JsonResponse({'data': data_dict,
                                    'msg': 'sucess'})
            else:
                user_objs_data = Users.objects.filter(member_email=memb_obj).filter(blood_group=selectedItem)
                serializers_user = UserSerializer(user_objs_data, many=True)
                data_dict = data_dict+serializers_user.data
                
                for objs in user_objs:
                    fam_data_obj = family.objects.filter(
                        user_id=objs).filter(blood_group=selectedItem)
                    serializers_fam = FamilySerializer(
                        fam_data_obj, many=True)
                    data_dict = data_dict+serializers_fam.data
                return JsonResponse({'data': data_dict,
                                        'msg': 'sucess'})
        else:
            return JsonResponse({'msg': 'no data found'})
    else:
        return JsonResponse({'msg': 'Invaild request'})



@csrf_exempt
def post_notification(request):
    if request.method == "POST":
        img_path = " "
        utype = request.POST['utype']
        token = request.POST['token']
        if utype == 'memb':
            user_obj = CustomUser.objects.get(session_token=token)
            if user_obj is not None:
                memb_obj = Member.objects.get(email=user_obj)
                name = request.POST['name']
                try:
                    img_path = request.FILES['img_path']
                except:
                    print("erorror")
                desc = request.POST['desc']
                status = '1'
                notifi_obj = Notification(
                    member_email=memb_obj, name=name, img_path=img_path, desc=desc, status=status)
                notifi_obj.save()
                return JsonResponse({'sucess': 'Notification registerd'})
            else:
                return JsonResponse({'error': 'Notification not  registerd'})
        else:
            return JsonResponse({'error': 'Not member type'})
    else:
        return JsonResponse({'error': 'Invaild Request'})


@csrf_exempt
def get_status(request):
    if request.method == "POST":
        id = int(request.POST['id'])
        print(id)
        com_objs = Comp.objects.get(id=id)
        print(com_objs.status)
        return JsonResponse({'msg': 'sucess',
                             'status': com_objs.status})
    else:
        return JsonResponse({'msg': 'error'})


@csrf_exempt
def closecomplaint(request):
    if request.method == "POST":
        id = int(request.POST['id'])
        com_objs = Comp.objects.get(id=id)
        com_objs.status = '3'
        com_objs.save()
        return JsonResponse({'msg': 'Complaint Closed'
                             })
    else:
        return JsonResponse({'msg': 'Invaild Request or user not Authenticated'})

@csrf_exempt
def complaint_status(request):
    if request.method=="POST":
        token=request.POST['token']
        obj = CustomUser.objects.get(session_token=token)
        user_obj = Users.objects.get(email=obj)               
        memb_obj=Member.objects.get(email=user_obj.member_email)
        comp_obj = Comp.objects.filter(member_email=memb_obj)
        opencomp = str(len(Comp.objects.filter(member_email=memb_obj,status='1')))
        pendingcomp =str(len (Comp.objects.filter(member_email=memb_obj,status='2')))
        closedcomp = str(len(Comp.objects.filter(member_email=memb_obj,status='3')))
        print(opencomp,pendingcomp,closedcomp)
        return JsonResponse({'status':{'opencomp': opencomp,
        'pendingcomp':pendingcomp,
        'closedcomp':closedcomp}
                             })
    else:
        return JsonResponse({'msg': 'Invaild Request or user not Authenticated'})


@csrf_exempt
def update_complaint(request):
    print("___"*100)
    if request.method == "POST":
        utype = request.POST['utype']
        id = int(request.POST['id'])
        remark = request.POST['remark']
        com_obj = Comp.objects.get(id=id)
        comment_obj = Comments(complaint_id=com_obj,
                               user=utype, comment=remark)
        com_objs = Comp.objects.get(id=id)
        if com_objs.status != '3' and utype=="memb":
            com_objs.status = '2'
            com_objs.save()
        comment_obj.save()
        return JsonResponse({'msg': 'sucess'
                             })

    else:
        return JsonResponse({'msg': 'Invaild Request or user not Authenticated'})


@csrf_exempt
def fam_memb_reg(request):
    if request.method == "POST":
        utype = request.POST['utype']
        token = request.POST['token']
        if utype == "user":
            user_email = CustomUser.objects.get(session_token=token).email
            user_obj = Users.objects.get(email=user_email)
            if user_obj is not None:
                email = request.POST['email']
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                voter_id = request.POST['voter_id']
                job = request.POST['job']
                tax_payer = request.POST['tax_payer']
                age = int(request.POST['age'])
                gender = request.POST['gender']
                phone = request.POST['phone']
                blood_group = request.POST['blood_group']
                qualification = request.POST['qualification']
                relation = request.POST['relation']

                fam_obj = family(email=email, firstname=firstname, lastname=lastname, voter_id=voter_id, job=job,
                                 tax_payer=tax_payer, age=age, gender=gender, phone=phone, blood_group=blood_group,
                                 qualification=qualification, user_id=user_obj, relation=relation)
                fam_obj.save()
                return JsonResponse({"msg": "family member registered"})
            else:
                return JsonResponse({'msg': 'Invalid session'})
        else:
            return JsonResponse({'msg': 'Invalid user'})
    else:
        return JsonResponse({'msg': 'Invaild request'})
