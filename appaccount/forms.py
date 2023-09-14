from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(forms.ModelForm):
    # email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("user_id", "user_pw")