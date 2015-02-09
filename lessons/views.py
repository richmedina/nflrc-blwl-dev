from django.views.generic import TemplateView, DetailView, UpdateView
from django import forms

from braces.views import LoginRequiredMixin

from core.mixins import HonorCodeRequired
from .models import Module, Lesson, LessonSection, PbllPage
from .forms import ModuleUpdateForm, LessonUpdateForm, LessonSectionUpdateForm, PbllPageUpdateForm

class HomeView(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['pbllpage'] = PbllPage.objects.get(pk=1)
		context['modules'] = Module.objects.all()
		return context

class ModuleView(LoginRequiredMixin, HonorCodeRequired, DetailView):
	model = Module
	template_name = 'module.html'

	def get_context_data(self, **kwargs):
		context = super(ModuleView, self).get_context_data(**kwargs)
		context['lessons'] = self.get_object().lessons.all()
		return context

class LessonView(LoginRequiredMixin, HonorCodeRequired, DetailView):
	model = Lesson
	template_name = 'lesson.html'
	context_object_name = 'lesson'

	def get_context_data(self, **kwargs):
		context = super(LessonView, self).get_context_data(**kwargs)
		
		try:
			quiz_url = self.get_object().lesson_quiz.get().quiz.url
			context['quiz'] =  quiz_url
		except:
			pass
		
		try:
			context['curr_section'] = self.kwargs['section']
		except:
			context['curr_section'] = 'topic'

		context['section_items'] = self.get_object().sections.filter(content_type=context['curr_section'])
		
		try:
			context['lesson_thread'] =  self.get_object().lesson_discussion.get().thread.slug
			preview_replies = self.get_object().lesson_discussion.get().thread.replies.all().filter(deleted=False).order_by('-modified')
			context['lesson_thread_replies'] = preview_replies[0:1]
		except:
			context['lesson_thread'] = None

		context['module_lessons'] = self.get_object().module.lessons.all()
		return context

class PbllPageView(DetailView):
	model = PbllPage
	template_name = "pbllpage.html"


class ModuleUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
	model = Module
	template_name = "edit_form.html"
	form_class = ModuleUpdateForm

	def get_context_data(self, **kwargs):
		context = super(ModuleUpdateView, self).get_context_data(**kwargs)
		context['object_type'] = 'Module'
		return context

class LessonUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
	model = Lesson
	template_name = "edit_form.html"
	form_class = LessonUpdateForm

	def get_context_data(self, **kwargs):
		context = super(LessonUpdateView, self).get_context_data(**kwargs)
		context['object_type'] = 'Lesson'
		return context

class LessonSectionUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
	model = LessonSection
	template_name = "edit_form.html"
	form_class = LessonSectionUpdateForm

	def get_context_data(self, **kwargs):
		context = super(LessonSectionUpdateView, self).get_context_data(**kwargs)
		context['object_type'] = self.get_object().content_type 
		return context

class LoginForbiddenView(TemplateView):
	template_name = 'login-forbidden.html'

class PbllPageUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
	model = PbllPage
	template_name = "edit_form.html"
	form_class = PbllPageUpdateForm

	def get_context_data(self, **kwargs):
		context = super(PbllPageUpdateView, self).get_context_data(**kwargs)
		context['object_type'] = 'Generic Page'
		return context

