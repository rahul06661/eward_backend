from rest_framework import routers
from django.urls import path,include


router=routers.DefaultRouter()
from . import views

urlpatterns = [
   # path('memb_home/',views.memb_home,name='membhome'),
    path('get_comp/',views.get_complaint,name='getcomplaint'),
    path('get_noti/',views.get_notification,name="getnotifications"),
    path('post_comp/',views.post_complaint,name="postcomplaint"),
    path('post_noti/',views.post_notification,name="postnotifications"),
    path('update_comp/',views.update_complaint,name="update_complaint"),
    path('family_memb_reg/',views.fam_memb_reg,name="fam_memb_reg")
    
]