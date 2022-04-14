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
    path('aboutus', views.aboutus, name='aboutus'),
    path('loginPage', views.loginPage, name='login'),
    path('labLogin', views.labLogin, name='labLogin'),
    path('doctorlogin', views.doctorlogin, name='doctorlogin'),
    path('help', views.help, name='help'),
    path('signup', views.signup, name='signup'),
    path('doctors', views.doctors, name='doctors'),
    path('search_doc', views.search_doc, name='search_doc'),
    path('depDoctor<int:aid>', views.depDoctor, name='depDoctor'),
    path('department', views.department, name='department'),
    path('booking', views.booking, name='booking'),
    path('docBooking<int:aid>', views.docBooking, name='docBooking'),
    path('userProfile', views.userProfile, name='userProfile'),
    path('userEdit<int:aid>', views.userEdit, name='userEdit'),
    path('doctorProfile', views.doctorProfile, name='doctorProfile'),
    path('labWorkshop', views.labWorkshop, name='labWorkshop'),
    path('conformation', views.conformation, name='conformation'),
    path('medicalReport<int:aid>', views.medicalReport, name='medicalReport'),
    path('logout', views.logout, name='logout'),
    path('load-doctor', views.load_doctor, name='ajax_load_doctor'),

    path('render_pdf_view<int:aid>', views.render_pdf_view, name='render_pdf_view'),
    path('render_pdf_blood<int:aid>',
         views.render_pdf_blood, name='render_pdf_blood'),
    path('render_pdf_Mri<int:aid>',
         views.render_pdf_Mri, name='render_pdf_Mri'),
    path('render_pdf_endoscopy<int:aid>',
         views.render_pdf_endoscopy, name='render_pdf_endoscopy'),
    path('render_pdf_Xray<int:aid>',
         views.render_pdf_Xray, name='render_pdf_Xray'),

    path('delete_appointment<int:aid>',
         delete_appointment, name='delete_appointment'),
    path('delete_user',
         delete_user, name='delete_user'),

    # Lab Reports
    path('bloodReport<int:aid>',
         views.bloodReport, name='bloodReport'),
    path('mriReport<int:aid>',
         views.mriReport, name='mriReport'),
    path('endoscopyReport<int:aid>',
         views.endoscopyReport, name='endoscopyReport'),
    path('xrayReport<int:aid>',
         views.xrayReport, name='xrayReport'),

    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('footer', views.footer, name='footer'),
    #     path('navbar', views.navbar, name='navbar'),

    path('api/verify_payment', verify_payment, name='verify_payment')
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
