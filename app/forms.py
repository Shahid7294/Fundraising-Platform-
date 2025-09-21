from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth import password_validation
from .models import Donor,Volunteer,Donation ,DonationArea

class LoginForm(AuthenticationForm):
    username = UsernameField(required=True,widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control','placeholder':'Username'}))
    password = forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
class Userform(UserCreationForm):
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password'}))
    password2 = forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Password Again'}))
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password1','password2']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter user name'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter last name'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter email name'}),
        }
class Donersingupform(forms.ModelForm):
    userpic=forms.ImageField(widget=forms.TextInput(attrs={'class':'form-control'})),
    class Meta:
        model=Donor
        fields=['contact','userpic','address'] 
        widgets={
            'contact':forms.NumberInput(attrs={'class':'form-control','placeholder':'Contact Number'}),
            'address':forms.Textarea(attrs={'class':'form-control','placeholder':'full Address'}),
        }
class voluntersingupform(forms.ModelForm):
    userpic=forms.ImageField(),
    idpic=forms.ImageField(),
    class Meta:
        model=Volunteer
        fields=['contact','userpic','idpic','address','aboutme']
        widgets={
            'contact':forms.NumberInput(attrs={'class':'form-control','placeholder':'Contact Number'}),
            'address':forms.Textarea(attrs={'class':'form-control','placeholder':'Full Address'}),
            'aboutme':forms.Textarea(attrs={'class':'form-control','placeholder':'About Me'}),
            'userpic':forms.FileInput(attrs={'class':'form-control'}),
            'idpic':forms.FileInput(attrs={'class':'form-control'}),
        }
        labels={
            'userpic':'User Picture',
            'Idpic':'Id Prodect Picture'
        }
class MyPasswordChangeForm(PasswordChangeForm):
    old_password= forms.CharField(label='Old Password', strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control','placeholder':'old password'}))
    new_password1 =forms.CharField(label='New Password',strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control','placeholder':'new password'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm New Password',strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control','placeholder':'confirm password'}))
# forget password
class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(label="Email",max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))
class MySetPasswordForm(SetPasswordForm):
    new_password1 =forms.CharField(label='New Password',strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control','placeholder':'new password'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label='Confirm New Password',strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control','placeholder':'confirm password'}))

DONATION_CHOICES=(
    ('Food Donation','Food Donation'),
    ('Cloth Donation','Cloth Donation'),
    ('Footwear Donation','Footwear Donation'),
    ('Books Donation','Books Donation'),
    ('Furniture Donation','Furniture Donation'),
    ('Vessel Donation','Vessel Donation'),
    ('Other Donation','Other Donation'),
)
class DonateNowForm(forms.ModelForm):
    class Meta:
        model= Donation
        fields=['donationname','donatiopic','collectionloc','description']
        widgets={
            'donationname':forms.Select(choices=DONATION_CHOICES,attrs={'class':'form-control'}),
            'collectionloc':forms.TextInput(attrs={'class':'form-control','placeholder':'Donation Collection Addres'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Description (Special Note)'}),
            'donatiopic':forms.FileInput(attrs={'class':'form-control'})
        }
        labels={
            'donatiopic':'Donation Image(Pic of Items u want to donate',
            'donationname':'Donation Name',
            'collectionloc':'Donation Collection Address',
            'description':'Description (Special) Note'
        }

class DonationAreaForm(forms.ModelForm):
    class Meta:
        model=DonationArea
        fields=['areaname','description']
        widgets={
            'areaname':forms.TextInput(attrs={'class':'form-control','placeholder':'Donation Area'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Description'})
        }
        labels={
            'areaname':'Donation Area Name',
            'description':'Description',
        }
    
 