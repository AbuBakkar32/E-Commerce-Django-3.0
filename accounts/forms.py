
from django import forms  
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from .models import UserProfile

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('full_name', 'email')
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('passwrod2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password don't match!")
        return password2
    
    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user  
    
    
    
    
    
class UserAdminChangeform(forms.ModelForm):
    
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User  
        fields = ('email', 'full_name', 'password', 'is_active', 'admin')
        
        
    def clean_password(self):
        return self.initial['password']



class GuestForm(forms.Form):
     email = forms.EmailField(widget=forms.EmailInput(
                                                    attrs={
                                                        'placeholder': 'Email Address',
                                                        'id': 'guest_email'
                                                    }
                                                )
                                            )

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
                                                'placeholder': 'Email Address',
                                                'id': 'login-email'
                                            }
                                        ),label="Email Address"
                                    )
    password = forms.CharField(widget=forms.PasswordInput(
                                            attrs={
                                                'placeholder': 'Password',
                                                'id': 'login-password'
                                            }
                                        )   
                                    )




class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
                                            attrs={
                                                    'id':'register-password', 
                                                    'placeholder': 'Password'
                                            }),help_text="i. Passwords must be at least 5 characters.<br>i. Passwords must be at least 1 number.<br>i. Passwords length must be at least 6 or more")
    
    password2 = forms.CharField(label='Re-enter password', widget=forms.PasswordInput(
                                            attrs={
                                                 'id': 'register-password2',
                                                'placeholder': 'Password Confirm'
                                            }))
    
    class Meta:
        model = User
        fields = ( 'email','full_name')
        widgets = {
            'email': forms.EmailInput(attrs={'id': 'register-email', 'placeholder':'Email Address'}),
            'full_name': forms.TextInput(attrs={'id': 'register-fullname', 'placeholder': 'Full Name'})
        }
        
        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        print(password1,password2)
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) <= 5:
            raise forms.ValidationError('Password length must be at least 6 charecter!')
        return password1

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False
        if commit:
            user.save()
        return user
     
Gen_choices = (
    ('male', 'Male'),
    ('female', 'Female')
)

YEARS = [x for x in range(1930, 2016)]


class UserProfileForm(forms.ModelForm):
    gender = forms.CharField(initial="male", widget=forms.RadioSelect(choices=Gen_choices))
    date_of_birth = forms.DateField(initial="2000-02-01", widget=forms.SelectDateWidget(years=YEARS))
    class Meta:
        model = UserProfile
        fields = [
            'profile_img',
            'gender',
            'date_of_birth',
            'mobile_number'
        ]

class UserEdit(forms.ModelForm):
    class Meta:
        model = User 
        fields = ['full_name', 'email']

YEARS = [x for x in range(1930, 2020)]
class UserProfileEdit(forms.ModelForm):
    date_of_birth = forms.DateField(initial="2000-02-01", widget=forms.SelectDateWidget(years=YEARS))
    class Meta:
        model = UserProfile 
        fields = ['gender', 'date_of_birth', 'mobile_number','profile_img']






        