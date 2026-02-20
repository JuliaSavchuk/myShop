from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Ім'я",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Введіть ваше ім'я"
        }),
        error_messages={
            'required': "Це поле є обов'язковим.",
            'max_length': "Максимальна довжина — 100 символів."
        }
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        }),
        error_messages={
            'required': "Це поле є обов'язковим.",
            'invalid': "Введіть коректну email-адресу."
        }
    )

    subject = forms.CharField(
        max_length=200,
        label="Тема",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Тема повідомлення'
        }),
        error_messages={
            'required': "Це поле є обов'язковим."
        }
    )

    message = forms.CharField(
        label="Повідомлення",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Ваше повідомлення...'
        }),
        error_messages={
            'required': "Це поле є обов'язковим."
        }
    )

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise ValidationError("Ім'я повинно містити щонайменше 2 символи.")
        if name.isdigit():
            raise ValidationError("Ім'я не може складатися лише з цифр.")
        return name

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise ValidationError("Повідомлення повинно містити щонайменше 10 символів.")
        if message.count('http') > 3:
            raise ValidationError("Повідомлення містить занадто багато посилань.")
        return message

    def clean_subject(self):
        return self.cleaned_data.get('subject', '').strip()