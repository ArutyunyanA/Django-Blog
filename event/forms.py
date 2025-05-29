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
            validate_image_format(image)
        return image

class EventCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body', 'parent']
        widgets = {'parent': forms.HiddenInput()}