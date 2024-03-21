from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('loginpage/',views.user_login, name='loginpage'),
    path('register/',views.user_register, name='register'),
    # path('update_profile/',views.update_profile, name='update_profile')
    path('create-profile/', views.create_profile, name='create_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile_detail/', views.profile_detail, name='profile_detail'),
    path('profile/edit/', views.edit_profile, name='profile_edit'),
    path("main/",views.main,name='main')

    
 
]