from django.contrib import admin
from .models import User, Job, JobImages
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','full_name','is_active','is_staff')
    list_filter = ('is_active','is_staff')

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id','title','location','description','status')
    list_filter = ('status',)

@admin.register(JobImages)
class JobImagesAdmin(admin.ModelAdmin):
    list_display = ('job','image','uploaded_at',)
    list_filter = ('job','uploaded_at',)
