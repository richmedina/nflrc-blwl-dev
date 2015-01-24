# lessons/forms.py
from django import forms

from .models import Module, Lesson, LessonSection

class ModuleUpdateForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 80, 'class': 'editor'}),
             
        }
        
       

class LessonUpdateForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'description', 'active']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 80, 'class': 'editor'}),

        }
        
       

class LessonSectionUpdateForm(forms.ModelForm):
    class Meta:
        model = LessonSection
        fields = ['text', 'content_type']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'cols': 80, 'class': 'editor'}),
        }    