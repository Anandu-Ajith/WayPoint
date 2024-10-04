from django import forms
from .models import *

class DestinationForm(forms.ModelForm):
    class Meta:
        model=Destination
        fields= '__all__'