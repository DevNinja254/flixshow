from django.contrib import admin
from .models import Type, VideoUpload, Cartegories, HomepageVideo,videos

# Register your models here.

admin.site.register(Type)
admin.site.register(VideoUpload)
admin.site.register(Cartegories)
admin.site.register(HomepageVideo)
admin.site.register(videos)