from django.urls import path
from . import views

urlpatterns = [
    path('main_comp/',views.main_comp,name='main_comp'),
    path('create/', views.create_job, name='create_job'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'), 
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('joblist_com/', views.job_list_com, name='joblist_com'),

]

    

