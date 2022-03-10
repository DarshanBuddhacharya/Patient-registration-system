from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from registration.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact', views.contact, name='contact'),
    path('loginPage', views.loginPage, name='login'),
    path('labLogin', views.labLogin, name='labLogin'),
    path('doctorlogin', views.doctorlogin, name='doctorlogin'),
    path('help', views.help, name='help'),
    path('signup', views.signup, name='signup'),
    path('doctors', views.doctors, name='doctors'),
    path('department', views.department, name='department'),
    path('booking', views.booking, name='booking'),
    path('userProfile', views.userProfile, name='userProfile'),
    path('doctorProfile', views.doctorProfile, name='doctorProfile'),
    path('labWorkshop', views.labWorkshop, name='labWorkshop'),
    path('conformation', views.conformation, name='conformation'),
    path('medicalReport<int:aid>', views.medicalReport, name='medicalReport'),
    path('logout', views.logout, name='logout'),
    path('load-doctor', views.load_doctor, name='ajax_load_doctor'),
    path('render_pdf_view<int:aid>', views.render_pdf_view, name='render_pdf_view'),
    path('delete_appointment<int:aid>',
         delete_appointment, name='delete_appointment'),

    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('footer', views.footer, name='footer'),

    path('api/verify_payment', verify_payment, name='verify_payment')
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
