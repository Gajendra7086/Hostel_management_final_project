"""hostelproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginpage),
    path('login_details/', views.login_details),
    path('hostel_register/', views.hostel_register),
    path('hostel_admin/', views.hostel_admin),
    path('hostler/', views.hostler),
    path('hostel_admin/hostel_details/', views.hostel_details),
    path('hosteler/hosteler_details/', views.hosteler_details),
    path('emailGeneration/', views.emailGeneration),
    path('emailValidation/', views.emailValidation),
    path('hostel_admin/verify_hostlers_page/', views.verify_hostlers_page),
    path('hostel_admin/verify_hostler/<str:id>', views.verify_hostler),
    path('hostel_admin/delete_verify_hostler/<str:id>', views.delete_verify_hostler),
    path('hostel_admin/add_hostler/', views.add_hostler),
    path('hostel_admin/payment/', views.hostel_admin_payment),
    path('hostel_admin/payment_list/',views.hostel_admin_payment_list),
    path('hostler/complain/', views.hostler_complain),
    path('hostel_admin/all_hostler/', views.all_hostler),
    path('hostler/complain_status/', views.hostler_complain_status),
    path('hostel_admin/complain/', views.hostel_admin_complains),
    path('change_complain_status/<str:id>', views.change_complain_status),
    path('change_password/', views.change_password),
    path('hostler/receipt/', views.payment_receipt),
    path('forgot_password/', views.forgot_password),
    path('logout/', views.logout_user),
    # ajax
    path('check_hostler_email/', views.check_hostler_email),
    path('hostelNameChecker/', views.hostelNameChecker),
]
