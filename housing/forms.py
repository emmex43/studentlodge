# housing/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none',
        'placeholder': 'Your Full Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none',
        'placeholder': 'your.email@example.com'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none',
        'placeholder': 'How can we help you?',
        'rows': 5
    }))