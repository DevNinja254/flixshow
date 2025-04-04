from django.db import models
from .manage import CustomUserManager 
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
import random, uuid
# All members
class Members(AbstractUser):
    username = models.CharField(max_length=100, unique=True, default=random.randint(1, 10000000))
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    class Meta:
        db_table = "members"

def generate_unique_id():
    return uuid.uuid4()


class Profile(models.Model):
    # BuyerID = models.BigAutoField(auto_created=True, primary_key=True)
    buyerid = models.UUIDField(primary_key=True, default=generate_unique_id, editable=False)
    username = models.CharField(max_length=200, default=generate_unique_id, editable=True)
    user = models.OneToOneField(Members, on_delete=models.CASCADE, related_name="profile", default="false")
    account = models.IntegerField(verbose_name="account(Ksh)", default=0,)    
    phone_number = models.IntegerField(default="0700000000")
    country = models.CharField(max_length=100, default="Kenya")
    city = models.CharField(max_length=100, default="mombasa")
    profile_pic = models.ImageField(upload_to="profile_pics/", default="profile_pics/download.png")
    def __str__(self):
        return self.user.username 
    class Meta:
        db_table = "profile"
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_profile, sender=Members)
post_save.connect(save_profile, sender=Members)

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
    video_id = models.IntegerField(default=1)
    cost = models.CharField(max_length=150, default=0)
    watcher = models.CharField(max_length=150, default = "aga")
    image_url = models.URLField(default="https://images.unsplash.com/photo-1604545200457-63641121af3b?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGRhcmVkZXZpbHxlbnwwfHwwfHx8MA%3D%3D")

    def __str__(self):
        return self.watcher
    class Meta:
        db_table = "watch"
class Cart(models.Model):
    username = models.CharField(max_length=150, default="user")
    video_id = models.IntegerField(default=1)
    video_name = models.CharField(max_length=150)
    price = models.IntegerField(default='0')
    cartegory = models.CharField(max_length=150, default="cartegory")
    type = models.CharField(max_length=100, default="type")
    season = models.CharField(max_length=100, default="full")
    image_url = models.URLField(default="https://images.unsplash.com/photo-1604545200457-63641121af3b?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGRhcmVkZXZpbHxlbnwwfHwwfHx8MA%3D%3D")
    def __str__(self):
        return self.username
    class Meta:
        db_table = "cart"
class Purchased(models.Model):
    video_id = models.IntegerField(default=1)
    username = models.CharField(max_length=150, default="user")
    video_name = models.CharField(max_length=150)
    image_url = models.URLField(default="https://images.unsplash.com/photo-1604545200457-63641121af3b?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGRhcmVkZXZpbHxlbnwwfHwwfHx8MA%3D%3D")
    price = models.IntegerField()
    purchase_time = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.username
    class Meta:
        db_table = "purchased"
class DownloadHistory(models.Model):
    video_id = models.IntegerField(default=1)
    name = models.CharField(max_length=150)
    video_name = models.CharField(max_length=150)
    cost = models.CharField(max_length=150, default=0)
    image_url = models.URLField(default="https://images.unsplash.com/photo-1604545200457-63641121af3b?w=400&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fGRhcmVkZXZpbHxlbnwwfHwwfHx8MA%3D%3D")
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

class Paymentcodes(models.Model):
    code = models.CharField(max_length=150)
    amount = models.IntegerField()

    def __str__(self):
        return self.code
class BettingRecords(models.Model):
    bet_id = models.UUIDField(editable=False, primary_key=True, default=generate_unique_id)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="betting_record")
    username = models.CharField(max_length=150, default=uuid.uuid1())
    betting_date = models.DateTimeField(default=timezone.now)
    win = models.IntegerField()
class Errors(models.Model):
    error_id = models.UUIDField(default=generate_unique_id, primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="errors")
    error_details = models.TextField()
