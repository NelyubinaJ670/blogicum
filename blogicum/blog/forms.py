from django import forms

from .models import Post, Comment, User


class PostForm(forms.ModelForm):
    """Форма публикаций."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].empty_label = 'Местоположение не выбрано'
        self.fields['category'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%d %H:%M:%S',
                attrs={'type': 'datetime-local'}
            )
        }


class CommentForm(forms.ModelForm):
    """Форма для комментария"""
    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
