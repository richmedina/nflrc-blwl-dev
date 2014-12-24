# discussions/forms.py
from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['subject', 'text', 'creator', 'parent_post']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
            'creator': forms.HiddenInput(),
            'parent_post': forms.HiddenInput(), 
        }
        labels = {
            'text': ''
        }
