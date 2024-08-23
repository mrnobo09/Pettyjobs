from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError

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


class Job(models.Model):
    WAITING = 'waiting'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    REJECTED = 'rejected'

    MECHANICAL = 'mechanical'
    ELECTRICAL = 'electrical'

    status_choices = [
        (WAITING,'Waiting'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED,'Completed'),
        (REJECTED,'Rejected')
    ]

    job_choices = [
        (MECHANICAL, 'Mechanical'),
        (ELECTRICAL, 'Electrical'),
    ]

    id = models.AutoField(null=False,primary_key=True)
    title = models.CharField(max_length = 500)
    job_type = models.CharField(max_length = 255,choices=job_choices,default=MECHANICAL)
    location = models.CharField(max_length = 500)
    description = models.CharField(max_length = 2000)
    status = models.CharField(max_length=50,choices=status_choices,default=WAITING)

    approved_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='approved_by',default=None)
    accepted_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'accepted_by',default=None)

    def save(self):
        if self.approved_by and self.approved_by.user_type != User.IN_CHARGE:
            raise ValidationError(f"The user must be of type '{User.IN_CHARGE}' to approve a job")
        if self.accepted_by and self.accepted_by.user_type != User.WORKER:
            raise ValidationError(f"The user must be of type '{User.WORKER}' to approve a job")
        
        super().save()

    def __str__(self):
        return str(self.id) + ". " + self.title

class JobImages(models.Model):
    job = models.ForeignKey(Job,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='jobs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

