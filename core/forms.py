from django import forms

class PNRForm(forms.form):
    pnr = forms.CharField(max_length=10, label="Enter your PNR")