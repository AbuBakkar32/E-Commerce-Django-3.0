from django import forms 

from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            # 'billing_profile',
            # 'address_type',
            'full_name',
            'mobile_number',
            'address_line_1',
            'address_line_2',
            'city',
            'country',
            'state',
            'postal_code'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'id':'full_name','placeholder': 'Full Name'}),
            'mobile_number': forms.NumberInput(attrs={'id':'mobile_no','placeholder': '+8801xxx-xxxxxx'}),
            'address_line_1': forms.TextInput(attrs={'id':'address_line_1','placeholder': 'Street Address, P.O, company name'}),
            'address_line_2': forms.TextInput(attrs={'id':'address_line_2','placeholder': 'Apartment, Unit, building, floor etc..'}),
            'city': forms.TextInput(attrs={'id':'city','placeholder': 'City name'}),
            'country': forms.TextInput(attrs={'id':'country','placeholder': 'Country name'}),
            'state': forms.TextInput(attrs={'id':'state','placeholder': 'State name'}),
            'postal_code': forms.TextInput(attrs={'id':'postal_code','placeholder': 'Postal code'})
        }

