from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .form import CustomUserCreationForm, CustomUserChangeForm
from .models import Members,Buyers, Onwatch, Payment, DepositHistory, DownloadHistory,Cart, Message

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Members
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
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
    search_fields = ("email",)
    ordering = ("email",)
    class Meta:
        db_table = "Members"

admin.site.register(Members, CustomUserAdmin)
admin.site.register(Buyers)
admin.site.register(Onwatch)
admin.site.register(Payment)
admin.site.register(DepositHistory)
admin.site.register(DownloadHistory)
admin.site.register(Cart)
admin.site.register(Message)
