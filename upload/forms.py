from django import forms

class DocumentForm(forms.Form):
    title = forms.CharField(max_length=50)
    docfile = forms.Field(
    label = 'Select a file')
