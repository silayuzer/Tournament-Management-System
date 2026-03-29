from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    password_confirm=forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model=User
        fields=['email', 'password']

    def clean(self):
        cleaned_data=super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data