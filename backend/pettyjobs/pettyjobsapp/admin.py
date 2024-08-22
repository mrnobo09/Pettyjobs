from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username','full_name','is_active','is_staff')
    list_filter = ('is_active','is_staff')
