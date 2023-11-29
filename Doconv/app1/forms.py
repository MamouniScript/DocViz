from django import forms
from .models import UploadedFile
from django.core.validators import FileExtensionValidator

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

class VisualizationForm(forms.Form):
    selected_column_name = forms.CharField(widget=forms.HiddenInput(), required=False)
    column_name = forms.ChoiceField(choices=[], label='Select a Column')
    visualization_type = forms.ChoiceField(choices=[], label='Select a Visualization Type')

    def __init__(self, *args, **kwargs):
        column_choices = kwargs.pop('column_choices', [])
        visualization_choices = kwargs.pop('visualization_choices', [])

        super(VisualizationForm, self).__init__(*args, **kwargs)

        self.fields['column_name'].choices = column_choices
        self.fields['visualization_type'].choices = visualization_choices
