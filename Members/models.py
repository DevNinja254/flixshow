from django.db import models
from .manage import CustomUserManager 
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.conf import settings

# All members
class Members(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    def __str__(self):
        return self.email
    class Meta:
        db_table = "members"   
class Buyers(Members):
    BuyerID = models.BigAutoField(auto_created=True,unique=True, primary_key=True)
    username = models.CharField(max_length=150, null=False, unique=True)
    account = models.IntegerField(verbose_name="account(Ksh)", default=0,)    
    phone_number = models.IntegerField(default="0700000000")
    country = models.CharField(max_length=100, default="Kenya")
    city = models.CharField(max_length=100, default="mombasa")
    profile = models.ImageField(upload_to="profile_pics/", default="profile_pics/download.png")
    def __str__(self):
        return self.username  
    class Meta:
        db_table = "buyers"
class Message(models.Model):
    message_id = models.BigAutoField(auto_created=True, primary_key=True)
    email = models.EmailField(max_length=100, blank=False)
    message = models.TextField()
    def __str__(self):
        return self.email 
    class Meta:
        db_table = "messages"
class Onwatch(models.Model):
    video_name = models.CharField(max_length=150)
    watcher = models.CharField(max_length=150, default = "aga")
    start_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.watcher
    class Meta:
        db_table = "watch"
class Cart(models.Model):
    username = models.CharField(max_length=150, default="user")
    video_name = models.CharField(max_length=150)
    def __str__(self):
        return self.username
    class Meta:
        db_table = "cart"
class DownloadHistory(models.Model):
    name = models.CharField(max_length=150)
    video_name = models.CharField(max_length=150)
    cost = models.CharField(max_length=150, default=0)
    time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "downloads"
class DepositHistory(models.Model):
    name = models.CharField(max_length=150)
    amount = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name
    class Meta:
        db_table = "deposit" 
class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email
    class Meta:
        db_table = "passreset"
class Payment(models.Model):
    username = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=150)
    payment_Suc = models.BooleanField(default=False)
    def __str__(self):
        return self.username
    class Meta:
        db_table = "payments"
class Notification(models.Model):
    message = models.TextField()
    date_notified = models.DateTimeField(auto_now_add=True)
