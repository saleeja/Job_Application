from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_job, name='create_job'),
    path('edit/<int:job_id>/', views.edit_job, name='edit_job'), 
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('joblist/', views.job_list, name='job_list'),

]

    

