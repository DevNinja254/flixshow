from .models import Members
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Members
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Members
        fields = "__all__"