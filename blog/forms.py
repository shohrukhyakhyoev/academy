from django import forms

from blog.models import Post
from tinymce.widgets import TinyMCE


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            attrs={'required': False, 'cols': 30, 'rows': 10, "class": "input-field"}
        )
    )

    title = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Write a title to a post",
            "class": "input-field",
        }))

    overview = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Write an overview to a post",
            "class": "input-field",
        }))

    class Meta:
        model = Post
        fields = ['title', 'overview', 'content', 'thumbnail']
