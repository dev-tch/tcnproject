from django import forms
from .models import Office

class OfficeCreationForm(forms.ModelForm):
    class Meta:
        model = Office
        fields = ['ref', 'name', 'country', 'state', 'region', 'address' , 'number_of_windows']
