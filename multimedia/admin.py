from django.contrib import admin
from .models import Type, VideoUpload, Cartegories as Cartegorie,videos as Video
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CartegoryEdit(admin.ModelAdmin):
    list_display=("cartId", "cartName")
    search_fields=("cartName",)
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()


class VideoUploadEdit(admin.ModelAdmin):
    list_display=("title","price", "season", "cartegory", "typs", "date_uploaded")
    search_fields=("title", "season", "typs")
    readonly_fields = ("date_uploaded",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ("date_uploaded",)

class VideoEdit(admin.ModelAdmin):
    list_display=("name", "quality")
    search_fields=("name",)
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()

admin.site.register(VideoUpload, VideoUploadEdit)
admin.site.register(Cartegorie, CartegoryEdit)
admin.site.register(Video, VideoEdit)