from django import forms
from django.forms import ModelForm
from author.models import Author


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

    def clean_surname(self):
        cleaned_name = self.cleaned_data.get('surname')
        if cleaned_name.strip() == '':
            raise forms.ValidationError("The author's surname can not contain only spaces")
        return cleaned_name
