from django.urls import path
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('contact', views.contact),
    path('loginPage', views.loginPage, name='login'),
    path('help', views.help),
    path('signup', views.signup, name='signup'),
    path('doctors', views.doctors, name='doctors'),
    path('booking', views.booking, name='booking'),
    path('userProfile', views.userProfile, name='userProfile'),
    path('logout', views.logout, name='logout')
]

urlpatterns = urlpatterns + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
