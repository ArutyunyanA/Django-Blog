from django import forms
from django.forms.widgets import DateInput, TimeInput
from .models import Event, EventParticipant, Comment
from .validators import validate_image_format


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'image', 'description', 'country', 'region', 'city', 'date', 'time']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Insert the event name',
                'class': 'form-control',
            }),
            'date': DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'time': TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'country': forms.TextInput(attrs={
                'placeholder': 'Country',
                'class': 'form-control',
            }),
            'region': forms.TextInput(attrs={
                'placeholder': 'Region',
                'class': 'form-control',
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'City',
                'class': 'form-control',
            }),
        }
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


class EventCommentForm(forms.ModelForm):
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