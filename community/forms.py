
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from django.forms.widgets import PasswordInput, TextInput
from tinymce.widgets import TinyMCE

from community.models import Question, Answer, QuestionComment, AnswerComment


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))


class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class QuestionForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            attrs={'required': False, 'cols': 30, 'rows': 10, 'class': "content"}
        )
    )

    title = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "title",
    }))

    class Meta:
        model = Question
        fields = ('title', 'content', 'tag', )


class AnswerForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(
            attrs={'required': False, 'cols': 25, 'rows': 10, "label": "sfd"}
        )
    )

    class Meta:
        model = Answer
        fields = ('content',)


class QuestionCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "q_comment-text-form",
            "id": "q-comment",
            "placeholder": "Leave a comment"
        }), label='')

    class Meta:
        model = QuestionComment
        exclude = ('user', 'timestamp', 'question', )


class AnswerCommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "a_comment-text-form",
            "id": "a-comment",
            "placeholder": "Leave a comment"
        }), label='')

    class Meta:
        model = AnswerComment
        exclude = ('user', 'timestamp', 'answer', )