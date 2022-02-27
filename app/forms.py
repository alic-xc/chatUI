from django import forms
from django.contrib.auth import password_validation


class RegistrationForm(forms.Form):
    """ Company registration form """

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    confirm_password = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        password_validation.validate_password(password=password)

        if password != confirm_password:
            raise forms.ValidationError({
                'password': ['The two password didn\'t match']
            })

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class ChatRoomForm(forms.Form):
    title = forms.CharField(required=False)