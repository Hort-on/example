from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=100)
    middle_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


class UpdateYourselfForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    middle_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)


class UpdateUserForm(forms.Form):
    role = forms.IntegerField()
    is_active = forms.BooleanField(required=False)
