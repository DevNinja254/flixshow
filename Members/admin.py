from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Members,Profile, Onwatch, Paymentcodes, BettingRecords, Errors, DepositHistory, DownloadHistory,Cart, Message, Notification, Purchased
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Members
    list_display = ("email","username", "is_staff", "is_superuser",)
    list_filter = ("is_staff", "is_active","is_superuser")
    search_fields = ("email", "username")
    readonly_fields = ("date_joined",'is_approved')
    fieldsets = (
        (None, {"fields": ("email",)}),
        ("Permissions", {"fields": ("is_staff", "date_joined", "groups", "user_permissions")}),
    )
    list_display_links = ('email',)
    list_editable = ["username", "is_superuser", "is_staff"]
    ordering = ("-date_joined",)
    class Meta:
        db_table = "Members"


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


class Paymentcod(admin.ModelAdmin):
    list_display = ("code", "amount",)
    search_fields = ["code"]
class Buyer(admin.ModelAdmin):
    list_display = ("user",'account', "username")
    search_fields = ["username"]
class ErrosSetting(admin.ModelAdmin):
    list_display = ("error_id", "error_details")
    search_fields = ["error_id"]
class BettingSetting(admin.ModelAdmin):
    list_display = ("bet_id","username", 'betting_date', "win")
    search_fields = ["username"]
class PurchasedAdmin(admin.ModelAdmin):
    list_display = ("username", "video_name", "purchase_time", "price")
    search_fields = ["username"]
    list_filter = ("purchase_time",)
    ordering = ("-purchase_time",)
    list_editable = ["video_name", "username"]
    readonly_fields = ("purchase_time",)
admin.site.register(Members, CustomUserAdmin)
admin.site.register(Profile, Buyer )
admin.site.register(Onwatch, OnwatchEdit)
admin.site.register(DepositHistory, DepositHistoryEdit)
admin.site.register(DownloadHistory, DownloadHistoryEdit)
admin.site.register(Cart, CartsEdit)
admin.site.register(Message, MessageEdit)
admin.site.register(Notification)
admin.site.register(Paymentcodes, Paymentcod)
admin.site.register(Purchased, PurchasedAdmin)
admin.site.register(BettingRecords, BettingSetting)
admin.site.register(Errors, ErrosSetting)
