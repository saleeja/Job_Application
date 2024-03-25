from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('loginpage/',views.user_login, name='loginpage'),
    path('register/',views.user_register, name='register'),
    path('otp-verification/', views.otp_verification, name='otp_verification'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile_detail/', views.profile_detail, name='profile_detail'),
    path('profile/edit/', views.edit_profile, name='profile_edit'),
    path("main_seeker/",views.main_seeker,name='main_seeker'),
    path("main_page/",views.main_page,name='main_page'),
    path('logout_view/',views.logout_view,name='logout_view'),
    path('create_company_profile/', views.create_company_profile, name='create_company_profile'),
    path('com_profile_detail/', views.com_profile_detail, name='com_profile_detail'),
    path('com_update_profile/', views.com_update_profile, name='com_update_profile'),
    path('com_edit_profile/', views.com_edit_profile, name='com_edit_profile'),
    path('job_list/', views.job_list, name='job_list'),
    path('job_search/', views.job_search, name='job_search'),
    path('applied_job_list/',views.applied_job_list, name='applied_job_list'),
    path('job_list/', views.job_list_com, name='job_list'),
    path('apply_to_job/<int:job_id>/', views.apply_job, name='apply_to_job'),
    path('job_applications/', views.job_applications, name='job_applications'),
    path('job_application_status/<int:application_id>/', views.application_status, name='job_application_status'),
    # path('', views.main_comp, name='main_comp'),
    path('create_profile/<str:user_type>/', views.create_profile, name='create_profile'),
    path('job/search/', views.job_search, name='job_search'),
    path('admin_main/', views.admin_main, name='admin_main'),
    path('newly_joined_users/', views.newly_joined_users, name='newly_joined_users'),
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin_job_listings/', views.admin_job_listings, name='admin_job_listings'),
    path('edit_job_listing/<int:listing_id>/edit/', views.edit_job_listing, name='edit_job_listing'),
    path('delete_job_listing/<int:listing_id>/delete/', views.delete_job_listing, name='delete_job_listing'),
    path('approve_job_listing/<int:listing_id>/approve/', views.approve_job_listing, name='approve_job_listing'),
    path('reported_issues/', views.reported_issues, name='reported_issues'),
    path('issue_detail/<int:issue_id>/', views.issue_detail, name='issue_detail'),
    path('resolve_issue/<int:issue_id>/resolve/', views.resolve_issue, name='resolve_issue'),
    path('analytics/user-activity/', views.user_activity_report, name='user_activity_report'),





  

]