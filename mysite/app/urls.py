from django.urls import path
from app import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.userlogin,name='userlogin'),
    path('dashboard/',views.dashboard,name='dashboard'),
]
