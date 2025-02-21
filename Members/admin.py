from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .form import CustomUserCreationForm, CustomUserChangeForm
from .models import Members,Buyers, Onwatch, Payment, DepositHistory, DownloadHistory,Cart, Message, Notification
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Members
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    search_fields = ("email", "username")
    readonly_fields = ("date_joined",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "date_joined", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    # search_fields = ("email",)
    ordering = ("email",)
    class Meta:
        db_table = "Members"

class BuyersEdit(UserAdmin):
    list_display=("username","email", "date_joined", "account")
    search_fields=("username", "email")
    readonly_fields = ("date_joined",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ("-date_joined",)


class DepositHistoryEdit(admin.ModelAdmin):
    list_display=("name","amount", "time",)
    search_fields=("name", "amount")
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ("time",)
    fieldsets = ()
    ordering = ("-time", )


class DownloadHistoryEdit(admin.ModelAdmin):
    list_display=("name","video_name", "cost", "time")
    search_fields=("name", "video_name")
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ("time",)
    fieldsets = ()
    ordering = ("-time",)

class CartsEdit(admin.ModelAdmin):
    list_display=("username","video_name")
    search_fields=("username", "video_name")
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()


class MessageEdit(admin.ModelAdmin):
    list_display=("email", "message")
    search_fields=("email",)
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()

class OnwatchEdit(admin.ModelAdmin):
    list_display=("watcher","video_name")
    search_fields=("watcher", "video_name")
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()



admin.site.register(Members, CustomUserAdmin)
admin.site.register(Buyers,BuyersEdit )
admin.site.register(Onwatch, OnwatchEdit)
admin.site.register(DepositHistory, DepositHistoryEdit)
admin.site.register(DownloadHistory, DownloadHistoryEdit)
admin.site.register(Cart, CartsEdit)
admin.site.register(Message, MessageEdit)
admin.site.register(Notification)
