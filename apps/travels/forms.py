from django import forms

class AccomodationForm(forms.Form):
    business_name = forms.CharField(max_length=32)
    accomodation_type = forms.IntegerField()
    address = forms.CharField(max_length=255)
    price_per_night =  forms.FloatField()
    check_in = forms.DateTimeField()
    check_out = forms.DateTimeField()

class UploadPictureForm(forms.Form):
    picture = forms.ImageField()