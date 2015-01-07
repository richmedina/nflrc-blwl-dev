from django.views.generic import TemplateView, DetailView

from braces.views import LoginRequiredMixin

from .models import Module, Lesson, LessonSection

class HomeView(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['modules'] = Module.objects.all()
		return context

class ModuleView(LoginRequiredMixin, DetailView):
	model = Module
	template_name = 'module.html'

	def get_context_data(self, **kwargs):
		context = super(ModuleView, self).get_context_data(**kwargs)
		context['lessons'] = self.get_object().lessons.all()
		return context

class LessonView(LoginRequiredMixin, DetailView):
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
			context['section_items'] = LessonSection.objects.filter(content_type=self.kwargs['section'])
		except:
			context['curr_section'] = 'topic'
			context['section_items'] = LessonSection.objects.filter(content_type='topic')		

		try:
			context['lesson_thread'] =  self.get_object().lesson_discussion.get().thread.slug
			preview_replies = self.get_object().lesson_discussion.get().thread.replies.all().order_by('-modified')
			context['lesson_thread_replies'] = preview_replies[0:5]
		except:
			context['lesson_thread'] = None

		return context


class HonorAgreementView(TemplateView):
	template_name = 'inactive.html'

class LoginForbiddenView(TemplateView):
	template_name = 'login-forbidden.html'
