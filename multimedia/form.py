from django import forms
from .models import VideoUpload, VideosFormGenerator


class VideoUploads(forms.ModelForm):
   
   class Meta:
      model = VideoUpload
      fields = ("title", "price", "cartegory", "typs", "image", "Quality", "display","season", "popular", "synopsis", )

class VideoForm(forms.ModelForm):

   class Meta:
      model = VideosFormGenerator
      fields = ("name", "video", "quality")