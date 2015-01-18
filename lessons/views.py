from django.views.generic import TemplateView, DetailView, UpdateView

from braces.views import LoginRequiredMixin

from core.mixins import HonorCodeRequired
from .models import Module, Lesson, LessonSection, PbllPage

class HomeView(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['page_content'] = PbllPage.objects.get(pk=1)
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
			preview_replies = self.get_object().lesson_discussion.get().thread.replies.all().order_by('-modified')
			context['lesson_thread_replies'] = preview_replies[0:5]
		except:
			context['lesson_thread'] = None

		return context

class PbllPageView(DetailView):
	model = PbllPage
	template_name = "pbllpage.html"


class ModuleUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
	model = Module
	template_name = "edit_form.html"
	fields = ['title', 'description']

class LessonUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
	model = Lesson
	template_name = "edit_form.html"
	fields = ['title', 'description']

class LessonSectionUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
	model = LessonSection
	template_name = "edit_form.html"
	fields = ['text', 'content_type']

class LoginForbiddenView(TemplateView):
	template_name = 'login-forbidden.html'

class PbllPageUpdateView(LoginRequiredMixin, HonorCodeRequired, UpdateView):
	model = PbllPage
	template_name = "edit_form.html"
	fields = ['title', 'content']
	labels = {
            'title': 'Editing a PBLL basic page:'
        }
