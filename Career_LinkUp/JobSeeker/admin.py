from django.contrib import admin
from .models import CustomUser,CompanyProfile,JobApplication

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type'] 

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CompanyProfile)
admin.site.register(JobApplication)




