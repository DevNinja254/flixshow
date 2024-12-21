from django import forms
from .models import VideoUpload, videos


class VideoUploads(forms.ModelForm):
   
   class Meta:
      model = VideoUpload
      fields = ("title", "price", "cartegory", "typs", "image", "Quality","size","season", "display", "popular", "synopsis", )

class VideoForm(forms.ModelForm):

   class Meta:
      model = videos
      fields = ("name", "video", "quality", )
