from django import forms 

from .models import MarkettingPreference

class MarkettingPreferenceForm(forms.Form):
    class Meta:
        model = MarkettingPreference
        fields = [
            'subscribed'
        ]

