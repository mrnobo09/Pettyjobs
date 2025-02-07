from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class UserAccountManager(BaseUserManager):
    def create_user(self, username, full_name, user_type, sub_type=None, password=None):
        if not username:
            raise ValueError("User must have a username")
        
        if user_type in [User.IN_CHARGE, User.CONTRACTOR] and not sub_type:
            raise ValueError("sub_type is required for user_type 'IN_CHARGE' or 'CONTRACTOR'")

        user = self.model(
            username=username,
            full_name=full_name,
            user_type=user_type,
            sub_type=sub_type,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, full_name, password=None):
        user = self.create_user(
            username=username,
            full_name=full_name,
            user_type=User.ADMIN, 
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    CONTRACTOR = 'contractor'
    WORKER = 'worker'
    IN_CHARGE = 'in_charge'
    ADMIN = 'admin'
    
    MECHANICAL = 'mechanical'
    ELECTRICAL = 'electrical'
    CIVIL = 'civil'

    USER_TYPE_CHOICES = [
        (CONTRACTOR, 'Contractor'),
        (IN_CHARGE, 'In Charge'),
        (WORKER, 'Worker'),
        (ADMIN, 'Admin')
    ]

    SUB_TYPE_CHOICES = [
        (MECHANICAL, 'Mechanical'),
        (ELECTRICAL, 'Electrical'),
        (CIVIL, 'Civil')
    ]
    
    id = models.AutoField(null=False, primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES,null=True,blank=True)
    sub_type = models.CharField(max_length=50, choices=SUB_TYPE_CHOICES, null=True, blank=True)

    score = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(10.0)
        ],
        null=True,
        blank=True,
        default=0.0,
    )
    
    objects = UserAccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']

    def save(self, *args, **kwargs):
        if self.user_type in [self.IN_CHARGE, self.CONTRACTOR] and not self.sub_type:
            raise ValidationError(f"sub_type is required for user_type '{self.user_type}'")
        super().save(*args, **kwargs)

    def getName(self):
        return self.full_name

    def __str__(self):
        return self.username


class Job(models.Model):
    WAITING = 'waiting'
    IN_PROGRESS = 'in_progress'
    REVIEW = 'review'
    FINAL = 'final'
    COMPLETED = 'completed'
    REJECTED = 'rejected'

    MECHANICAL = 'mechanical'
    ELECTRICAL = 'electrical'
    CIVIL = 'civil'

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH= 'high'


    status_choices = [
        (WAITING,'Waiting'),
        (IN_PROGRESS, 'In Progress'),
        (REVIEW,'Review'),
        (FINAL,'Final'),
        (COMPLETED,'Completed'),
        (REJECTED,'Rejected'),
    ]

    job_choices = [
        (MECHANICAL, 'Mechanical'),
        (ELECTRICAL, 'Electrical'),
        (CIVIL,'Civil')
    ]

    criticality_choices = [
        (LOW,'Low'),
        (MEDIUM,'Medium'),
        (HIGH,'High'),
    ]

    id = models.AutoField(null=False,primary_key=True)
    title = models.CharField(max_length = 500)
    job_type = models.CharField(max_length = 255,choices=job_choices,default=MECHANICAL)
    location = models.CharField(max_length = 500)
    description = models.CharField(max_length = 2000)
    status = models.CharField(max_length=50,choices=status_choices,default=WAITING)
    criticality = models.CharField(max_length=50,choices=criticality_choices,default=LOW)

    approved_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='approved_by',null=True,blank = True)
    accepted_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name = 'accepted_by',null = True,blank = True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_by',null = True,blank = True)

    uploaded_at = models.DateTimeField(default = timezone.now)
    approved_at = models.DateTimeField(null = True, blank=True)
    completed_at = models.DateTimeField(null = True, blank=True)

    pause = models.BooleanField(default=False)
    paused_at = models.DateTimeField(null = True,blank=True)
    resumed_at = models.DateTimeField(null = True,blank=True)

    total_pause_duration = models.DurationField(null = True,blank = True)

    def pause_job(self):
        if not self.paused_at:
            self.paused_at = timezone.now()
            self.pause = True
            self.save()

    def resume_job(self):
        if self.paused_at:
            pause_duration = timezone.now() - self.paused_at
            self.total_pause_duration += pause_duration
            self.paused_at = None
            self.resumed_at = timezone.now()
            self.pause = False
            self.save()


    def save(self,*args,**kwargs):
        if self.approved_by and self.approved_by.user_type != User.IN_CHARGE:
            raise ValidationError(f"The user must be of type '{User.IN_CHARGE}' to approve a job")
        if self.accepted_by and self.accepted_by.user_type != User.CONTRACTOR:
            raise ValidationError(f"The user must be of type '{User.CONTRACTOR}' to accept a job")
        if self.uploaded_by and self.uploaded_by.user_type != User.WORKER:
            raise ValidationError(f"User must be a {User.WORKER} to post a job")
        
        if self.completed_at and self.approved_at:
            total_duration = self.completed_at - self.approved_at
            self.duration = total_duration - self.total_pause_duration
        
        super().save(*args,**kwargs)

    def __str__(self):
        return str(self.id) + ". " + self.title

class JobImages(models.Model):
    job = models.ForeignKey(Job,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='jobs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    job = models.ForeignKey(Job, related_name='rating_from_worker', on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    contractor = models.ForeignKey(User, related_name='contractor_rating', on_delete=models.CASCADE)
    worker = models.ForeignKey(User, related_name='worker_rating', on_delete=models.CASCADE)

class Rating_2(models.Model):
    job = models.ForeignKey(Job, related_name='rating_from_incharge', on_delete=models.CASCADE)
    rating = models.FloatField(
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(10.0),
        ]
    )
    contractor = models.ForeignKey(User, related_name='contractor_rating_incharge', on_delete=models.CASCADE)
    in_charge = models.ForeignKey(User, related_name='incharge_rating', on_delete=models.CASCADE)



