from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
        labels = {
            'name':'',
            'body': '',  # Убираем метку для поля body
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control comment-name-input',
                                           'placeholder': 'Ваше имя'}),
            'body': forms.Textarea(attrs={'class': 'form-control comment-body-input',
                                          'placeholder': 'Напишите, что вы думаете...'}),
        }
