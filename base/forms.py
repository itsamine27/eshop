from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import User,CompanyModel
from products.models import CompanyProducts,CompanyProductsImages
class SignupUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']
    
class LogintUserForm(AuthenticationForm):
    pass

class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyModel
        fields = ['company_logo', 'company_slogan', 'discount_points']



class SearchCompany(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',  # Bootstrap class for styling
                'placeholder': 'Enter company name',  # Placeholder text
                'style': 'width: 300%; border-radius: 5px; padding: 10px;',  # Inline styling
            }
        ),
        label='Company Name',  # Adds a label for the field
    )
