from rest_framework import routers
from django.urls import path,include
from . import views

urlpatterns = [
    path('signin/', views.singin,name='signin'),
    path('signout/<int:id>/', views.signout,name='signout'),
    path('member_signup/',views.MemberRegisteration,name='member_reg'),
    path('get_member/',views.GetMembers,name='GetMembers'),
    path('user_signup/',views.UserRegisteration,name="user_reg"),
    path('regs_users/<int:id>/', views.list_users_approved,name="regsted"),
    path('not_regs_user/',views.list_users_not_approved,name="notreg"),
    path('approve/',views.approve,name="approve"),
    path('changepassword/',views.RestPassword,name="reset"),
    path("resetpass/",views.PasswordReset,name="request-password-reset"),
    path("password-reset/<str:encoded_pk>/<str:token>/",views.reset_password,name="reset-password"),
    
]