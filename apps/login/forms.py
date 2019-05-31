from django import forms

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=32, min_length=2)
    last_name = forms.CharField(max_length=32, min_length=2)
    username = forms.CharField(max_length=32, min_length=3)
    email = forms.EmailField()
    
