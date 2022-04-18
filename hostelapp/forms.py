from django import forms
from django.contrib.auth import authenticate
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password


class loginForm(forms.Form):
    username = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)


class user_creationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'mobile_no', 'is_warden_owner', 'hostel_name']
        widget = {
            'username': forms.EmailInput,
            'mobile_no': forms.NumberInput,
            'password': forms.PasswordInput,
            'is_warden_owner': forms.CheckboxInput,
        }

    def save(self, commit=True):
        user = super(user_creationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

