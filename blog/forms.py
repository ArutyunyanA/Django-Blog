from django import forms
from .models import Comment, Post
from .validators import validate_image_format


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
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            try:
                validate_image_format(image)
            except forms.ValidationError as err:
                raise err
            except Exception:
                raise forms.ValidationError("Downloaded file format do not acceptable.")
        return image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write a comment..."
            }),
        }

