from rest_framework import routers
from django.urls import path,include
from . import views

urlpatterns = [
    path('signin/', views.singin,name='signin'),
    path('signout/<int:id>/', views.signout,name='signout'),
    path('member_signup/',views.MemberRegisteration,name='member_reg'),
    path('user_signup/',views.UserRegisteration,name="user_reg"),
    path('regs_users/<int:id>/', views.list_users_approved,name="regsted"),
    path('not_regs_user/<int:id>/',views.list_users_not_approved,name="notreg")
    
]