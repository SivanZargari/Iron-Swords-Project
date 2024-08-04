# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Hero

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        # Call the parent method to handle the default validation
        super().confirm_login_allowed(user)
        # Check if the user is active. If not, raise a validation error with a custom message
        if not user.is_active:
            raise forms.ValidationError(
                "הסיסמא שגויה, נא לנסות שוב",  # Custom error message
                code='invalid_login'  # Error code
            )
        
class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ['first_name', 'last_name', 'age', 'hometown', 'country_of_birth', 'hero_story', 'image']
        labels = {
            'first_name': 'שם פרטי',  
            'last_name': 'שם משפחה',
            'age': 'גיל',
            'hometown': 'עיר מגורים',
            'country_of_birth': 'ארץ לידה',
            'hero_story': 'סיפור גבורה',
            'image': 'תמונה', 
        }
        widgets = {
            'image': forms.FileInput()  # Use FileInput for single file uploads
        }