# lessons/forms.py
from django import forms
from django.forms import inlineformset_factory
from django.forms.models import BaseModelFormSet
from django.forms.widgets import RadioSelect

from multichoice.models import MCQuestion, Answer
from .models import Project, Module, Lesson, LessonModule, LessonSection, PbllPage

# class ProjectUpdateForm(forms.ModelForm):
#     class Meta:
        

class ModuleCreateForm(forms.ModelForm):

    class Meta:
        model = Module
        fields = ['title', 'description', 'order', 'project']
        widgets = {
            'project': forms.HiddenInput(),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 80, 'class': 'form-control content-editor'}),      
        }


class ModuleUpdateForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'description', 'order']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 80, 'class': 'form-control content-editor'}),    
        }
        

class LessonCreateForm(forms.ModelForm):
    module = forms.ModelChoiceField(queryset=Module.objects.all(), widget=forms.HiddenInput())
    order_in_module = forms.IntegerField()

    class Meta:
        model = Lesson
        fields = ['creator', 'title', 'description', 'active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 80, 'class': 'form-control content-editor'}),
            'creator': forms.HiddenInput(),
        }


class LessonModuleCreateForm(forms.ModelForm):
    # module = forms.ModelChoiceField(queryset=Module.objects.all(), widget=forms.TextInput())
    # lessons = forms.ModelChoiceField(queryset=Lesson.objects.all(), widget=forms.Select())

    class Meta:
        model = LessonModule
        fields = ['lesson', 'module', 'order']
        widgets = {
            'module': forms.HiddenInput(),
        }


class LessonUpdateForm(forms.ModelForm):
    lesson_module_obj = forms.ModelChoiceField(queryset=LessonModule.objects.all(), widget=forms.HiddenInput)
    order_in_module = forms.IntegerField()

    class Meta:
        model = Lesson
        fields = ['creator', 'title', 'description', 'active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 80, 'class': 'form-control content-editor'}),
        }


class LessonSectionUpdateForm(forms.ModelForm):
    class Meta:
        model = LessonSection
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 25, 'cols': 80, 'class': 'form-control content-editor'}),
        }


class LessonQuizQuestionCreateForm(forms.ModelForm):   
    class Meta:
        model = MCQuestion
        fields = ['quiz', 'content', 'explanation']
        widgets = {
            'quiz': forms.MultipleHiddenInput(),
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'explanation': forms.Textarea(attrs={'rows': 5, 'cols': 40})
            }


AnswersCreateFormSet = inlineformset_factory(
    MCQuestion, Answer, 
    extra=5,
    fields=('question', 'content', 'correct'), 
    widgets={'content': forms.TextInput(attrs={'size': 40})},
    labels={'content': 'Text to display for this choice.'}
)


AnswersUpdateFormSet = inlineformset_factory(
    MCQuestion, Answer, 
    extra=3,
    can_delete=True,
    fields=('question', 'content', 'correct'), 
    widgets={'content': forms.TextInput(attrs={'size': 40})},
    labels={'content': 'Text to display for this choice.'}
)


class PbllPageUpdateForm(forms.ModelForm):
    class Meta:
        model = PbllPage
        fields = ['title', 'content']
        labels = {
            'title': 'Page title:'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 25, 'cols': 80, 'class': 'form-control content-editor'}),
        }