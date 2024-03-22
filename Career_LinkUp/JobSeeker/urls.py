from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('loginpage/',views.user_login, name='loginpage'),
    path('register/',views.user_register, name='register'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile_detail/', views.profile_detail, name='profile_detail'),
    path('profile/edit/', views.edit_profile, name='profile_edit'),
    path("main_seeker/",views.main_seeker,name='main_seeker'),
    path('logout_view/',views.logout_view,name='logout_view'),
    path('create_company_profile/', views.create_company_profile, name='create_company_profile'),
    path('com_profile_detail/', views.com_profile_detail, name='com_profile_detail'),
    path('com_update_profile/', views.com_update_profile, name='com_update_profile'),
    path('com_edit_profile/', views.com_edit_profile, name='com_edit_profile'),
    path('job_list/', views.job_list, name='job_list'),
    path('apply-to-job/<int:job_id>/', views.apply_to_job, name='apply_to_job'),
    path('job_search/', views.job_search, name='job_search'),
    path('job_application_status/', views.job_application_status, name='job_application_status'),


]