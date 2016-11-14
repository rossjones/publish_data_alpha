from django.utils.translation import ugettext as _
from django import forms

class SigninForm(forms.Form):
    email = forms.CharField(label=_('Email address'), max_length=100)
    password = forms.CharField(
        label=_('Password'),
        max_length=100,
        widget=forms.PasswordInput
    )