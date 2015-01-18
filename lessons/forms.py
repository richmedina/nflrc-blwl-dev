# lessons/forms.py
from django import forms

from .models import Module, Lesson, LessonSection

class ModuleUpdateForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']
        """
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
            'creator': forms.HiddenInput(),
            'parent_post': forms.HiddenInput(), 
        }
        labels = {
            'text': ''
        }
        """

class LessonUpdateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description']
        """
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
            'creator': forms.HiddenInput(),
            'parent_post': forms.HiddenInput(), 
        }
        labels = {
            'text': ''
        }
        """

class LessonSectionUpdateForm(forms.ModelForm):
    class Meta:
        model = LessonSection
        fields = ['title', 'description']
        """
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 80}),
            'creator': forms.HiddenInput(),
            'parent_post': forms.HiddenInput(), 
        }
        labels = {
            'text': ''
        }
        """