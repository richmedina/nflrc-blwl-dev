# forms.py
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from lessons.models import Project
from .models import Whitelist, ProjectMembership

class HonorCodeForm(ModelForm):
    
    class Meta:
    	model = Whitelist
    	fields = ['honor_agreement']
        labels = {
            'honor_agreement': _('I have read, acknowledge, and agree to the above statements'),
        }


class WhitelistCreateForm(ModelForm):
    membership = forms.ModelMultipleChoiceField(queryset=Project.objects.all(), required=False)

    class Meta:
        model = Whitelist
        fields = ['email_addr', 'membership']


class WhitelistUpdateForm(ModelForm):
    membership = forms.ModelMultipleChoiceField(queryset=Project.objects.all(), required=False)

    class Meta:
        model = Whitelist
        fields = ['email_addr', 'membership']


class ProjectParticipantCreateForm(ModelForm):
    class Meta:
        model = ProjectMembership
        fields = ['project', 'user']
        widgets = {'project': forms.HiddenInput(), 'user': forms.Select()}