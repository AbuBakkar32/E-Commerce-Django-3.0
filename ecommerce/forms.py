from django import forms  


class ContactForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Full Name',
                                        'id': 'full_name'
                                    }
                                )
                            )
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                                                'class': 'form-control',
                                                'placeholder': 'Email Address',
                                                'id': 'email'
                                            }
                                        ), label='Email Address'
                                    )
    message = forms.CharField(widget=forms.Textarea(attrs={
                                                'class': 'form-control',
                                                'placeholder': 'Your Messages..',
                                                'id': 'message'
                                            }
                                        )
                                    )

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'gmail.com' not in email:
            raise forms.ValidationError('Email has to be gmail!')
        return email 






    







