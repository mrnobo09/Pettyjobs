from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_user(self, username,full_name,user_type, password=None):
        if not username:
            raise ValueError("User must have a username")
        user = self.model(username = username, full_name = full_name,user_type = user_type)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self,username,full_name,password=None):
        user = self.create_user(username,full_name,password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    CONTRACTOR = 'contractor'
    WORKER = 'worker'
    IN_CHARGE = 'in_charge'
    

    USER_TYPE_CHOICES = [
        (CONTRACTOR, 'Contractor'),
        (IN_CHARGE, 'In Charge'),
        (WORKER,'Worker')
    ]   

    id = models.AutoField(null=False,primary_key=True)
    username = models.CharField(max_length=255,unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    user_type = models.CharField(max_length=50,choices=USER_TYPE_CHOICES)

    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name','user_type']

    def getName(self):
        return self.full_name
    
    def __str__(self):
        return self.username
