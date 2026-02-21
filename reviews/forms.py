from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f"{i} ★") for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'star-rating-input'}),
        label="Ваша оцінка"
    )

    class Meta:
        model = Review
        fields = ['rating', 'title', 'content', 'advantages', 'disadvantages']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Короткий заголовок відгуку',
                'class': 'review-input'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Детальний опис вашого досвіду...',
                'rows': 6,
                'class': 'review-textarea'
            }),
            'advantages': forms.Textarea(attrs={
                'placeholder': 'Переваги товару (необов’язково)',
                'rows': 3,
                'class': 'review-textarea'
            }),
            'disadvantages': forms.Textarea(attrs={
                'placeholder': 'Недоліки товару (необов’язково)',
                'rows': 3,
                'class': 'review-textarea'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 5:
            raise forms.ValidationError("Заголовок повинен містити мінімум 5 символів.")
        return title.strip()

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 20:
            raise forms.ValidationError("Текст відгуку повинен містити мінімум 20 символів.")
        return content.strip()

    def clean_advantages(self):
        return self.cleaned_data.get('advantages', '').strip()

    def clean_disadvantages(self):
        return self.cleaned_data.get('disadvantages', '').strip()