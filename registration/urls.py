from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('contact', views.contact),
    path('loginPage', views.loginPage, name='login'),
    path('help', views.help),
    path('signup', views.signup, name='signup'),
]
