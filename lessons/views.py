from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView

from .models import Lesson, LessonSection

class HomeView(TemplateView):
	template_name = 'index.html'

class LessonListView(ListView):
	model = Lesson
	template_name = 'lesson_list.html'

class LessonView(DetailView):
	model = Lesson
	template_name = 'lesson.html'

class IsotopeView(TemplateView):
	template_name = 'isotope_scratch.html'
