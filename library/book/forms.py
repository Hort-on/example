from django.forms import ModelForm
from book.models import Book
from django import forms


class BookAddForms(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'required': True}),
            'year_of_publication': forms.DateInput(attrs={'type': 'date'}),
            'date_of_issue': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_count(self):
        cleaned_count = self.cleaned_data.get('count')
        if cleaned_count < 1:
            raise forms.ValidationError('Count of books can not be less than 1')
        return cleaned_count

    def clean_name(self):
        cleaned_name = self.cleaned_data.get('name')
        if cleaned_name.strip() == '':
            raise forms.ValidationError('The book title can not contain only spaces')
        return cleaned_name


class BookSearchForms(forms.Form):
    choice = (
        ('0', 'author surname'),
        ('1', 'book title'),
    )
    select_fields = forms.ChoiceField(choices=choice, label='Find a book:')
    search_fields = forms.CharField(label=False, max_length=100)
