from django import forms
from .models import Comment, Post


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, required=False)

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'body', 'status', 'image', 'tags']
    image = forms.ImageField(required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body', 'parent']
        widgets = {'parent': forms.HiddenInput()}
