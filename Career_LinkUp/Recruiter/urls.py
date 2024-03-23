from django.urls import path
from . import views


urlpatterns = [
    path('main_comp/',views.main_comp,name='main_comp'),
    path('create/', views.create_job, name='create_job'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'), 
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('joblist_com/', views.job_list_com, name='joblist_com'),
    path('view_all_applicants/', views.view_all_applicants, name='view_all_applicants'),
    path('update_application_status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('resumes/<path:resume_path>/', views.serve_resume, name='serve_resume'),
]



   



    

