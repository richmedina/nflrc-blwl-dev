from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView

from .models import Stack

class HomeView(TemplateView):
	template_name = 'index.html'

class StackListView(ListView):
	model = Stack
	template_name = 'stack_list.html'

class StackView(DetailView):
	model = Stack
	template_name = 'stack.html'
