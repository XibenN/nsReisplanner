from django import forms

class reisplannerForm(forms.Form):
    beginstation = forms.CharField(required=True)
    eindstation = forms.CharField(required=True)