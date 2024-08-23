from django.contrib import admin
from .models import User, Job, JobImages
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','full_name','is_active','is_staff','user_type',)
    list_filter = ('is_active','is_staff','user_type',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('id','title','location','description','status','approved_by','accepted_by',)
    list_filter = ('status','approved_by','accepted_by',)

@admin.register(JobImages)
class JobImagesAdmin(admin.ModelAdmin):
    list_display = ('job','image','uploaded_at',)
    list_filter = ('job','uploaded_at',)
