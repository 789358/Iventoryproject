from django import forms
from .models import Item
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="メールアドレス")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }
        
class ContactForm(forms.Form):
    name = forms.CharField(label="お名前", max_length=100)
    email = forms.EmailField(label="メールアドレス")
    message = forms.CharField(label="メッセージ", widget=forms.Textarea)
