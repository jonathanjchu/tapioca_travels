from django import forms

class UploadAvatarForm(forms.Form):
    avatar = forms.ImageField()