from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField

# Create your models here.

class Cartegories(models.Model):
    cartId = models.BigAutoField(primary_key=True,auto_created=True)
    cartName = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.cartName
    
    class Meta:
        db_table = "cartegories"



class Type(models.Model):
    TYPE_CHOICES = [
        ('movies', 'Movies'),
        ("series", 'Series')
    ]
    typeId = models.BigAutoField(primary_key=True,auto_created=True)
    typeName = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.typeName
    
    class Meta:
        db_table = "types"
    def save(self, *args, **kwargs):
        self.typeName = self.name.capitalize()  # Convert name to lowercase
        super().save(*args, **kwargs)


class VideoUpload(models.Model):
    TYPE_CHOICES = [
        ('movies', 'Movies'),
        ("series", 'Series'),
    ]
 
    vidId = models.BigAutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=100, null=False, unique=True)
    price = models.IntegerField()
    cartegory = models.ForeignKey(Cartegories, to_field="cartName", on_delete=models.CASCADE)
    typs = models.CharField(choices=TYPE_CHOICES, verbose_name="video Type", default="movies", max_length=150)
    synopsis = models.TextField()
    date_uploaded = models.DateTimeField(default=timezone.now)
    image = ResizedImageField(size=[760, 420], upload_to="videoImage/")
    Quality = models.CharField(max_length=50)
    size = models.CharField(max_length=100, default="0mb")
    display = models.BooleanField( default=False)
    paid = models.BooleanField(default=False)
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
    video = models.FileField(upload_to="videos/")
    quality = models.CharField(max_length=100)
    ended = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()  # Convert name to capitalize
        super().save(*args, **kwargs)

    class Meta:
        db_table = "videos"


class HomepageVideo(models.Model):
    videoName = models.ForeignKey(VideoUpload, to_field="title", verbose_name="Select Video Name", default="movie", on_delete=models.CASCADE)

    class Meta:
        db_table = "homepagevideos"
