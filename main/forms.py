from .models import Search
from django.forms import ModelForm, TextInput


class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = ['search']

        widgets = {
            'search': TextInput(attrs={
                'class': "form-control",
                'placeholder': "Pro hledání prosím napište sem"
            })
        }
