from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField

# Create your models here.

class Cartegories(models.Model):
    cartId = models.BigAutoField(primary_key=True,auto_created=True)
    cartName = models.CharField(max_length=50, null=False, unique=True)
    cart_image = ResizedImageField(size=[760, 420], blank=True, null=True, upload_to="cartegories/", default="https://images.unsplash.com/photo-1579713899713-bcd3efe713aa?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
    def __str__(self):
        return self.cartName
    
    class Meta:
        db_table = "cartegories"


class VideoUpload(models.Model):
    TYPE_CHOICES = [
        ('movies', 'Movies'),
        ("series", 'Series'), 
        ("anime", 'Anime')
    ]
    vidId = models.BigAutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=100, null=False, unique=False)
    price = models.IntegerField()
    cartegory = models.ForeignKey(Cartegories, to_field="cartName", on_delete=models.CASCADE, related_name="video_details")
    typs = models.CharField(choices=TYPE_CHOICES, verbose_name="video Type", default="movies", max_length=150)
    synopsis = models.TextField()
    date_uploaded = models.DateTimeField(default=timezone.now)
    image = ResizedImageField(size=[760, 420], upload_to="videoImage/")
    season = models.CharField(max_length=150, default="season 2")
    popular = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.title = self.title.capitalize()  # Convert name to lowercase
        super().save(*args, **kwargs)
    class Meta:
        db_table = "uploads"

    

class videos(models.Model):
    videoId = models.BigAutoField(primary_key=True, auto_created=True)
    name=models.CharField(max_length=200, verbose_name="Enter Video Name", default="movie")
    video = models.FileField(upload_to="videos/", null=True)
    quality = models.CharField(max_length=100, null=True)
    size = models.CharField(max_length=100, default="0mb", null=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()  # Convert name to capitalize
        super().save(*args, **kwargs)

    class Meta:
        db_table = "videos"
    def delete(self):
        return self.video.delete()

class Like(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    user = models.CharField(max_length=150, default="anonymous")
    video_title = models.ForeignKey(VideoUpload, on_delete=models.CASCADE, related_name="likes")
    total_like = models.IntegerField()
    def __str__(self):
        return self.user 
class Review(models.Model) :
    id = models.BigAutoField(auto_created=True, primary_key=True)
    user = models.CharField(max_length=150, default="anonymous")
    video_title = models.ForeignKey(VideoUpload, on_delete=models.CASCADE, related_name="reviews")
    rate = models.IntegerField()
    comment = models.TextField()
    def __str__(self):
        return self.user
class AwaitingActivation(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True)
    username = models.CharField(max_length=100, default="user")
    video_name = models.CharField(max_length=100)
    price = models.IntegerField()
    date_entered = models.DateTimeField(default=timezone.now)
