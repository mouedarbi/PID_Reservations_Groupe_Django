from django import forms
from catalogue.models.setting import AppSetting

class AppSettingForm(forms.ModelForm):
    value = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), 
        required=False
    )

    class Meta:
        model = AppSetting
        fields = ['value', 'description']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }
