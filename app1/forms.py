from django import forms
from .models import UploadedFile
from django.core.validators import FileExtensionValidator

class FileUploadForm(forms.ModelForm):
    # Add hidden input field to store selected column name
    selected_column_name = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = UploadedFile
        fields = ['file']
