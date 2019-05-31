from django import forms
import datetime

class AccomodationForm(forms.Form):
    business_name = forms.CharField(max_length=32)
    accomodation_type = forms.IntegerField()
    address = forms.CharField(max_length=255)
    price_per_night =  forms.FloatField()
    check_in = forms.DateTimeField()
    check_out = forms.DateTimeField()

class UploadPictureForm(forms.Form):
    picture = forms.ImageField()

class LocationForm(forms.Form):
    # class Meta:
    #     model = MyModel
    #     fields = '__all__'
    #     widgets = {
    #         'my_date': DateInput()
    #     }

    name = forms.CharField(max_length=31)
    location_type = forms.CharField(max_length=15)
    fees = forms.FloatField()
    # start_time = forms.DateField(initial=datetime.date.today)
    # end_time = forms.DateTimeField(initial=datetime.date.today)
    information = forms.Textarea()


class DateInput(forms.DateInput):
    input_type = 'date'