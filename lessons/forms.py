# lessons/forms.py
from django import forms

from .models import Module, Lesson, LessonSection, PbllPage

class ModuleUpdateForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 80, 'class': 'form-control content-editor'}),
             
        }
        
       

class LessonUpdateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 80, 'class': 'form-control content-editor'}),

        }

class LessonSectionUpdateForm(forms.ModelForm):
    class Meta:
        model = LessonSection
        fields = ['text', 'content_type']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 25, 'cols': 80, 'class': 'form-control content-editor'}),
        }

class PbllPageUpdateForm(forms.ModelForm):
    class Meta:
        model = PbllPage
        fields = ['title', 'content']
        labels = {
            'title': 'Editing a PBLL basic page:'
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 25, 'cols': 80, 'class': 'form-control content-editor'}),
        }