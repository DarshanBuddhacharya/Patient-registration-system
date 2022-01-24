from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from registration.views import *

urlpatterns = [
    path('', views.index),
    path('contact', views.contact),
    path('loginPage', views.loginPage, name='login'),
    path('doctorlogin', views.doctorlogin, name='doclogin'),
    path('help', views.help),
    path('signup', views.signup, name='signup'),
    path('doctors', views.doctors, name='doctors'),
    path('booking', views.booking, name='booking'),
    path('userProfile', views.userProfile, name='userProfile'),
    path('doctorProfile', views.doctorProfile, name='doctorProfile'),
    path('conformation', views.conformation, name='conformation'),
    path('logout', views.logout, name='logout'),
    path('delete_appointment<int:aid>',
         delete_appointment, name='delete_appointment')
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
